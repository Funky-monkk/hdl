import os.path
from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst import Directive, directives
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util import logging
from lxml import etree
from adi_hdl_static import hdl_strings
import contextlib

logger = logging.getLogger(__name__)

class node_parameters(nodes.Structural, nodes.Element):
	pass

def dot_fix(string):
	if (string.rfind('.') != len(string)-1):
		return string + '.'
	else:
		return string

def pretty_dep(string):
	if string is None:
		return ''
	return string.replace("'MODELPARAM_VALUE.",'').replace("'",'')

def sanitized_bool(string):
	string_ = string.strip().lower()
	if string_ in ['1', 'true', 'yes', 'y']:
		return True
	elif string_ in ['0', 'false', 'no', 'n']:
		return False
	else:
		logger.warning(f"Got malformed bool value {string}.")
		return False

class directive_base(Directive):
	has_content = True
	add_index = True
	current_doc = ''
	final_argument_whitespace = True

	def warning(self, msg):
		logger.warning(msg + f" Current file: {self.current_doc}")
	def info(self, msg):
		logger.info(msg + f" Current file: {self.current_doc}")

	def get_descriptions(self, content):
		items = {}
		key = ''
		for line in content:
			if line.startswith('* -'):
				key = line[line.find('* -')+3:].split()[0]
				items[key] = []
			else:
				items[key].append(line)
		for key in items:
			items[key] = ' '.join(items[key]).strip().replace('- ', '', 1)
		return items

	def column_entry(self, row, text, node_type, classes=[]):
		entry = nodes.entry(classes=classes)
		if node_type == 'literal':
			entry += nodes.literal(text=text)
		elif node_type == 'paragraph':
			entry += nodes.paragraph(text=text)
		elif node_type == 'reST':
			rst = ViewList()
			rst.append(text, "virtual_"+self.current_doc, 0)
			node = nodes.section()
			node.document = self.state.document
			nested_parse_with_titles(self.state, rst, node)
			entry += node
		else:
			return
		row += entry

	def column_entries(self, rows, items):
		row = nodes.row()
		for item in items:
			if len(item) == 3:
				self.column_entry(row, item[0], item[1], classes=item[2])
			else:
				self.column_entry(row, item[0], item[1])
		rows.append(row)

	def generic_table(self, description):
		tgroup = nodes.tgroup(cols=2)
		for _ in range(2):
			colspec = nodes.colspec(colwidth=1)
			tgroup.append(colspec)
		table = nodes.table()
		table += tgroup

		self.table_header(tgroup, ["Name", "Description"])

		rows = []
		for key in description:
			row = nodes.row()
			entry = nodes.entry()
			entry += nodes.literal(text="{:s}".format(key))
			row += entry
			entry = nodes.entry()
			rst = ViewList()
			rst.append(description[key], "virtual_"+self.current_doc, 0)
			node = nodes.section()
			node.document = self.state.document
			nested_parse_with_titles(self.state, rst, node)
			entry += node
			row += entry
			rows.append(row)

		tbody = nodes.tbody()
		tbody.extend(rows)
		tgroup += tbody

		return table

	def table_header(self, tgroup, columns):
		thead = nodes.thead()
		tgroup += thead
		row = nodes.row()

		for header_name in columns:
			entry = nodes.entry()
			entry += nodes.paragraph(text=header_name)
			row += entry

		thead.append(row)

class directive_interfaces(directive_base):
	option_spec = {'path': directives.unchanged}
	required_arguments = 0
	optional_arguments = 0

	def tables(self, content, component):
		description = self.get_descriptions(content)

		if component is None:
			return self.generic_table(description)

		node_tables = nodes.section()

		bs = component['bus_interface']
		for tag in bs:
			section = nodes.section(ids=[f"bus-interface-{tag}"])
			title = nodes.title(text=tag)
			section += title
			if bs[tag]['dependency'] is not None:
				dependency = nodes.paragraph(text=f"Depends on {pretty_dep(bs[tag]['dependency'])}.")
				section += dependency
			if tag in description:
				rst = ViewList()
				rst.append(description[tag], "virtual_"+self.current_doc, 0)
				node = nodes.section()
				node.document = self.state.document
				nested_parse_with_titles(self.state, rst, node)
				section += node
			node_tables += section

			tgroup = nodes.tgroup(cols=3)
			for _ in range(3):
				colspec = nodes.colspec(colwidth=1)
				tgroup.append(colspec)
			table = nodes.table()
			table += tgroup

			self.table_header(tgroup, ["Physical Port", "Logical Port", "Direction"])

			rows = []
			pm = bs[tag]['port_map']
			for key in pm:
				self.column_entries(rows, [
					[key, 'literal'],
					[pm[key]['logical_port'], 'literal'],
					[pm[key]['direction'], 'paragraph'],
				])

			tbody = nodes.tbody()
			tbody.extend(rows)
			tgroup += tbody
			node_tables += table

		section = nodes.section(ids=[f"ports"])
		title = nodes.title(text="Ports")
		section += title
		node_tables += section
		tgroup = nodes.tgroup(cols=4)
		for _ in range(4):
			colspec = nodes.colspec(colwidth=1)
			tgroup.append(colspec)
		table = nodes.table()
		table += tgroup

		self.table_header(tgroup, ["Physical Port", "Direction", "Dependency", "Description"])

		rows = []
		pr = component['ports']
		for key in pr:
			row = nodes.row()
			self.column_entry(row, key, 'literal')
			self.column_entry(row, pr[key]['direction'], 'paragraph')
			self.column_entry(row, pretty_dep(pr[key]['dependency']), 'paragraph')
			if key in description:
				self.column_entry(row, description[key], 'reST', classes=['description'])
			else:
				self.column_entry(row, '', 'paragraph')
			rows.append(row)

		tbody = nodes.tbody()
		tbody.extend(rows)
		tgroup += tbody
		node_tables += table

		return node_tables

	def run(self):
		env = self.state.document.settings.env
		self.current_doc = env.doc2path(env.docname)

		node = node_parameters()

		if 'path' in self.options:
			lib_name = self.options['path']
		else:
			lib_name = env.docname.replace('/index', '')

		subnode = nodes.section(ids=["hdl-interfaces"])
		if lib_name in env.component:
			subnode += self.tables(self.content, env.component[lib_name])
		else:
			subnode += self.tables(self.content, None)

		node += subnode

		return [ node ]

class directive_regmap(directive_base):
	option_spec = {'name': directives.unchanged, 'no-type-info': directives.unchanged}
	required_arguments = 0
	optional_arguments = 0

	def tables(self, obj):
		node_tables = nodes.section()

		section = nodes.section(ids=[f"register-map-{obj['title-tool']}"])
		title = nodes.title(text=f"{obj['title']} ({obj['title-tool']})")
		section += title
		node_tables += section
		tgroup = nodes.tgroup(cols=7)
		for _ in range(7):
			colspec = nodes.colspec(colwidth=1)
			tgroup.append(colspec)
		table = nodes.table(classes=['regmap'])
		table += tgroup

		self.table_header(tgroup, ["DWORD", "BYTE", "BITS", "Name", "Type", "Default", "Description"])

		rows = []
		for reg in obj['regmap']:
			self.column_entries(rows, [
				[reg['address'][0], 'literal'],
				[reg['address'][1], 'literal'],
				['', 'literal'],
				[reg['name'], 'literal'],
				['', 'literal'],
				['', 'literal'],
				[reg['description'], 'reST', ['description']],
			])

			for field in reg['fields']:
				self.column_entries(rows, [
					['', 'literal'],
					['', 'literal'],
					[f"[{field['bits']}]", 'literal'],
					[field['name'], 'literal'],
					[field['rw'], 'paragraph'],
					[field['default'], 'paragraph'],
					[field['description'], 'reST', ['description']],
				])

		tbody = nodes.tbody()
		tbody.extend(rows)
		tgroup += tbody
		node_tables += table

		if 'no-type-info' in self.options:
			return node_tables

		tgroup = nodes.tgroup(cols=3)
		for _ in range(3):
			colspec = nodes.colspec(colwidth=1)
			tgroup.append(colspec)
		table = nodes.table()
		table += tgroup

		self.table_header(tgroup, ["Access Type", "Name", "Description"])

		rows = []
		for at in reg['access_type']:
			self.column_entries(rows, [
				[at, 'paragraph'],
				[hdl_strings.access_type[at]['name'], 'paragraph'],
				[hdl_strings.access_type[at]['description'], 'paragraph']
			])

		tbody = nodes.tbody()
		tbody.extend(rows)
		tgroup += tbody
		node_tables	+= table

		return node_tables

	def run(self):
		env = self.state.document.settings.env
		self.current_doc = env.doc2path(env.docname)
		if os.getcwd() not in self.current_doc:
			raise Exception(f"Inconsistent paths, {os.getcwd()} not in {self.current_doc}")
		owner = self.current_doc[len(os.getcwd())+1:-4]

		node = node_parameters()

		if 'name' in self.options:
			lib_name = self.options['name']
		else:
			self.warning("hdl-regmap directive without name option, skipped!")
			return [ node ]

		subnode = nodes.section(ids=["hdl-regmap"])
		if lib_name in env.regmaps:
			if owner not in env.regmaps[lib_name]['owners']:
				env.regmaps[lib_name]['owners'].append(owner)
			subnode += self.tables(env.regmaps[lib_name])
		else:
			self.warning(f"regmap/adi_regmap{lib_name}.txt not-found, skipped!")
			return [ node ]

		node += subnode
		return [ node ]

class directive_parameters(directive_base):
	option_spec = {'path': directives.unchanged}
	required_arguments = 0
	optional_arguments = 0

	def tables(self, content, parameter):
		description = self.get_descriptions(content)

		if parameter is None:
			return self.generic_table(description)

		tgroup = nodes.tgroup(cols=5)
		for _ in range(5):
			colspec = nodes.colspec(colwidth=1)
			tgroup.append(colspec)
		table = nodes.table()
		table += tgroup

		self.table_header(tgroup, ["Name", "Description", "Type", "Default Value", "Choices/Range"])

		rows = []
		for key in parameter:
			row = nodes.row()
			self.column_entry(row, "{:s}".format(key), 'literal')
			if key in description:
				self.column_entry(row, description[key], 'reST', classes=['description'])
			else:
				self.column_entry(row, dot_fix(parameter[key]['description']), 'paragraph', classes=['description'])
			for tag in ['type', 'default']:
				self.column_entry(row, parameter[key][tag].title(), 'paragraph')
			crange = []
			if parameter[key]['choices'] is not None:
				crange.append(parameter[key]['choices'])
			if parameter[key]['range'] is not None:
				crange.append(parameter[key]['range'])
			crange = '. '.join(crange)
			self.column_entry(row, crange, 'paragraph')

			rows.append(row)

		tbody = nodes.tbody()
		tbody.extend(rows)
		tgroup += tbody

		for tag in description:
			if tag not in parameter:
					self.warning(f"{tag} does not exist in {file_2}!")

		return table

	def run(self):
		env = self.state.document.settings.env
		self.current_doc = env.doc2path(env.docname)

		node = node_parameters()

		if 'path' in self.options:
			lib_name = self.options['path']
		else:
			lib_name = env.docname.replace('/index', '')

		subnode = nodes.section(ids=["hdl-parameters"])
		if lib_name in env.component:
			subnode += self.tables(self.content, env.component[lib_name]['parameters'])
		else:
			subnode += self.tables(self.content, None)

		node += subnode

		return [ node ]

def visit_node_parameters(self, node):
	pass

def depart_node_parameters(self, node):
	pass

def parse_hdl_component(path, ctime):
	component = {
		'bus_interface':{},
		'ports': {},
		'parameters': {},
		'ctime': ctime
	}

	def get_namespaces( item):
		nsmap = item.nsmap
		for i in ['spirit', 'xilinx', 'xsi']:
			if i not in nsmap:
				raise Exception(f"Required namespace {i} not in file!")

		return (nsmap['spirit'], nsmap['xilinx'], nsmap['xsi'])

	def get( item, local_name):
		items = get_all(item, local_name)
		if len(items) == 0:
			return None
		else:
			return items[0]

	def get_all( item, local_name):
		template = "/*[local-name()='%s']"
		if not isinstance(local_name, str):
			raise Exception("Got wrong type, only Strings are allowed")
		local_name = local_name.split('/')
		return item.xpath('.' + ''.join([template % ln for ln in local_name]))

	def sattrib( item, attr):
		nonlocal spirit
		return item.get(f"{{{spirit}}}{attr}")

	def xattrib( item, attr):
		nonlocal xilinx
		return item.get(f"{{{xilinx}}}{attr}")

	def stag( item):
		nonlocal spirit
		return item.tag.replace(f"{{{spirit}}}",'')

	def xtag( item):
		nonlocal xilinx
		return item.tag.replace(f"{{{xilinx}}}",'')

	def clean_dependency( string):
		return string[string.find("'"): string.rfind(')')].replace(')','')

	def get_dependency( item, type_=None):
		if type_ is None:
			type_ = stag(item)

		dependency = get(item, f"vendorExtensions/{type_}Info/enablement/isEnabled")
		if dependency is None:
			return None
		else:
			return clean_dependency(xattrib(dependency, 'dependency'))

	def get_range( item):
		min_ = sattrib(item, 'minimum')
		max_ = sattrib(item, 'maximum')
		if max_ == None or min_ == None:
			return None
		else:
			return f"From {min_} to {max_}."

	def get_choice_type( name):
		return name[name.find('_')+1:name.rfind('_')]

	root = etree.parse(path).getroot()
	spirit, xilinx, _ = get_namespaces(root)
	vendor = get(root, 'vendor').text
	name = get(root, 'name').text

	bs = component['bus_interface']
	for bus_interface in get_all(root, 'busInterfaces/busInterface'):
		bus_name = get(bus_interface, 'name').text
		bs[bus_name] = {
			'name': sattrib(get(bus_interface, 'busType'), 'name'),
			'dependency': get_dependency(bus_interface, 'busInterface'),
			'port_map': {}
		}

		pm = bs[bus_name]['port_map']
		for port_map in get_all(bus_interface, 'portMaps/portMap'):
			pm[get(port_map, 'physicalPort/name').text] = {
				'logical_port': get(port_map, 'logicalPort/name').text,
				'direction': ''
			}

	lport = component['ports']
	for port in get_all(root, 'model/ports/port'):
		port_name = get(port, 'name').text
		port_direction = get(port, 'wire/direction').text

		found = False
		for bus in bs:
			if port_name in bs[bus]['port_map']:
				found = True
				bs[bus]['port_map'][port_name]['direction'] = port_direction
				break;

		if found == False:
			lport[port_name] = {
				'direction': port_direction,
				'dependency': get_dependency(port, 'port')
			}
	pr = component['parameters']
	for parameter in get_all(root, 'parameters/parameter'):
		param_description = get(parameter, 'displayName')
		if param_description is not None:
			param_name = get(parameter, 'name').text
			param_value = get(parameter, 'value')
			pr[param_name] = {
				'description': param_description.text,
				'default': param_value.text,
				'type': sattrib(param_value, 'format'),
				'_choice_ref': sattrib(param_value, 'choiceRef'),
				'choices': None,
				'range': get_range(param_value)
			}

	for choice in get_all(root, 'choices/choice'):
		name = get(choice, 'name').text
		for key in pr:
			if pr[key]['_choice_ref'] == name:
				type_ = get_choice_type(name)
				values = get_all(choice, 'enumeration')
				string = []
				if type_ == 'pairs':
					for v in values:
						string.append(f"{sattrib(v, 'text')} ({v.text})")
				elif type_ == 'list':
					for v in values:
						string.append(v.text)
				else:
					break
				pr[key]['choices'] = ', '.join(string)
				break

	return component

def manage_hdl_components(env, docnames, libraries):
	if not hasattr(env, 'component'):
		env.component = {}
	cp = env.component
	for lib in list(cp):
		f = f"../{lib}/component.xml"
		if not os.path.isfile(f):
			del cp[lib]

	for lib, doc in libraries:
		f = f"../{lib}/component.xml"
		if not os.path.isfile(f):
			continue
		ctime = os.path.getctime(f)
		if lib in cp and cp[lib]['ctime'] >= ctime:
			pass
		else:
			cp[lib] = parse_hdl_component(f, ctime)
			docnames.append(doc)

# From https://github.com/tfcollins/vger/blob/main/vger/hdl_reg_map.py
def parse_hdl_regmap(reg, ctime):
	regmap = {
		'title': '',
		'title_tool': '',
		'regmap': [],
		'owners':[],
		'ctime': ctime
	}

	with open(f"regmap/adi_regmap_{reg}.txt", "r") as f:
		data = f.readlines()
	data = [d.replace("\n", "") for d in data]

	# Get title
	i = data.index("TITLE") + 1
	regmap['title'] = data[i].strip()
	regmap['title-tool'] = data[i + 1].strip()
	data = data[i + 1 :]

	# Get registers
	access_type = []
	while "REG" in data:
		rfi = data.index("ENDREG")
		regi = data.index("REG")
		reg_addr = data[regi + 1].strip()
		reg_name = data[regi + 2].strip()
		reg_desc = [data[fi].strip() for fi in range(regi + 3, rfi)]
		reg_desc = " ".join(reg_desc)

		data = data[regi + 1 :]

		# Get fields
		fields = []
		while "FIELD" in data:
			fi = data.index("FIELD")
			efi = data.index("ENDFIELD")

			if not fi:
				break

			with contextlib.suppress(ValueError):
				if rege := data.index("REG"):
					if fi > rege:
						# into next register
						break

			field_loc = data[fi + 1].strip()
			field_loc = field_loc.split(" ")
			field_bits = field_loc[0].replace("[", "").replace("]", "")
			field_default = field_loc[1] if len(field_loc) > 1 else "NA"

			field_name = data[fi + 2].strip()
			field_rw = data[fi + 3].strip()

			if field_rw == 'R':
				field_rw = 'RO'
			elif field_rw == 'W':
				field_rw = 'WO'
			if '-V' in field_rw:
				if 'V' not in access_type:
					access_type.append('V')
			field_rw_ = field_rw.replace('-V','')
			if field_rw_ not in access_type:
				if field_rw_ not in hdl_strings.access_type:
					logger.warning(f"Malformed access type {field_rw} for register {field_name}, file regmap/adi_regmap_{reg}.txt.")
				else:
					access_type.append(field_rw)

			field_desc = [data[fi].strip() for fi in range(fi + 4, efi)]
			field_desc = " ".join(field_desc)

			fields.append(
				{
					"name": field_name,
					"bits": field_bits,
					"default": field_default,
					"rw": field_rw,
					"description": field_desc,
				}
			)

			data = data[fi + 1 :]

		try:
			if '+' in reg_addr:
				reg_addr_ = reg_addr.split('+')
				reg_addr_[0] = int(reg_addr_[0], 16)
				reg_addr_[1] = int(reg_addr_[1].replace('*n',''), 16)
				reg_addr_dword = f"{hex(reg_addr_[0])} + {hex(reg_addr_[1])}*n"
				reg_addr_byte = f"{hex(reg_addr_[0]<<2)} + {hex(reg_addr_[1]<<2)}*n"
			else:
				reg_addr_ = int(reg_addr, 16)
				reg_addr_dword = f"{hex(reg_addr_)}"
				reg_addr_byte = f"{hex(reg_addr_<<2)}"
		except:
			logger.warning(f"Got malformed register address {reg_addr} for register {reg_name}, file regmap/adi_regmap_{reg}.txt.")
			reg_addr_dword = ""
			reg_addr_byte = ""

		regmap['regmap'].append(
			{
				'name': reg_name,
				'address': [reg_addr_dword,	reg_addr_byte],
				'description': reg_desc,
				'fields': fields,
				'access_type': access_type
			}
		)
	return regmap

def manage_hdl_regmaps(env, docnames):
	if not hasattr(env, 'regmaps'):
		env.regmaps = {}

	rm = env.regmaps
	for lib in list(rm):
		f = f"regmap/adi_regmap_{lib}.txt"
		if not os.path.isfile(f):
			del rm[lib]
	# Inconsistent naming convention, need to parse all in directory.
	files = []
	for (dirpath, dirnames, filenames) in os.walk("regmap"):
		files.extend(filenames)
		break
	regmaps = [f.replace('adi_regmap_','').replace('.txt','') for f in files]
	for reg_name in regmaps:
		ctime = os.path.getctime(f"regmap/adi_regmap_{reg_name}.txt")
		if reg_name in rm and rm[reg_name]['ctime'] < ctime:
			for o in rm[reg_name]['owners']:
				if o not in docnames:
					docnames.append(o)
		if reg_name in rm and rm[reg_name]['ctime'] >= ctime:
			pass
		else:
			rm[reg_name] = parse_hdl_regmap(reg_name, ctime)

def manage_hdl_artifacts(app, env, docnames):
	libraries =  [[k.replace('/index',''), k] for k in env.found_docs if k.find('library/') == 0]

	manage_hdl_components(env, docnames, libraries)
	manage_hdl_regmaps(env, docnames)

def setup(app):
	app.add_directive('hdl-parameters', directive_parameters)
	app.add_directive('hdl-interfaces', directive_interfaces)
	app.add_directive('hdl-regmap', directive_regmap)

	app.add_node(node_parameters,
			html=(visit_node_parameters, depart_node_parameters),
			latex=(visit_node_parameters, depart_node_parameters),
			text=(visit_node_parameters, depart_node_parameters))

	app.connect('env-before-read-docs', manage_hdl_artifacts)

	return {
		'version': '0.1',
		'parallel_read_safe': True,
		'parallel_write_safe': True,
	}
