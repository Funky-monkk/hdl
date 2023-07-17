from docutils import nodes
import subprocess

def get_active_branch_name():
	branch = subprocess.run(['git', 'branch', '--show-current'], capture_output=True)
	return branch.stdout.decode('utf-8').replace('\n','')

def git(repo):
	def role(name, rawtext, text, lineno, inliner, options={}, content=[]):

		app = inliner.document.settings.env.app
		try:
			if not app.config.git_org_url:
				raise AttributeError
		except AttributeError as err:
			raise ValueError('git_org_url configuration value is not set (%s)' % str(err))
		branch = get_active_branch_name() if text.find(':') in [0, -1] else text[0:text.find(':')]
		path = text[text.find(':')+1:]
		url = app.config.git_org_url + '/' + repo + '/blob/' + branch + '/' + path
		node = nodes.reference(rawtext, path[path.rfind('/')+1:], refuri=url, **options)
		return [node], []
	return role

def setup(app):
	app.add_role("git-hdl", git('hdl'))
	app.add_role("git-testbenches", git('testbenches'))
	app.add_role("git-linux", git('linux'))
	app.add_config_value('git_org_url', None, 'env')

	return {
		'version': '0.1',
		'parallel_read_safe': True,
		'parallel_write_safe': True,
	}
