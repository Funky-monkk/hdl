source ../../../scripts/adi_env.tcl
source ../../scripts/adi_project_intel.tcl

 adi_project ad9081_fmca_ebz_intel_ip_fm87

source $ad_hdl_dir/projects/common/fm87/fm87_system_assign.tcl

set_global_assignment -name VERILOG_FILE $ad_hdl_dir/projects/common/fm87/sgpio_slave.v

#execute_flow -compile
