
# Instances and instance parameters
add_instance gmii_to_rgmii_adapter_0 altera_gmii_to_rgmii_adapter
set_instance_parameter_value gmii_to_rgmii_adapter_0 {RX_PIPELINE_DEPTH} {1}
set_instance_parameter_value gmii_to_rgmii_adapter_0 {TX_PIPELINE_DEPTH} {1}

add_instance hps_emac_interface_splitter_0 altera_hps_emac_interface_splitter

add_instance gmii_to_rgmii_adapter_1 altera_gmii_to_rgmii_adapter
set_instance_parameter_value gmii_to_rgmii_adapter_1 {RX_PIPELINE_DEPTH} {1}
set_instance_parameter_value gmii_to_rgmii_adapter_1 {TX_PIPELINE_DEPTH} {1}

add_instance hps_emac_interface_splitter_1 altera_hps_emac_interface_splitter

add_instance iopll_0 altera_iopll
set_instance_parameter_value iopll_0 {gui_active_clk} {0}
set_instance_parameter_value iopll_0 {gui_c_cnt_in_src0} {c_m_cnt_in_src_ph_mux_clk}
set_instance_parameter_value iopll_0 {gui_c_cnt_in_src1} {c_m_cnt_in_src_ph_mux_clk}
set_instance_parameter_value iopll_0 {gui_cal_error} {cal_clean}
set_instance_parameter_value iopll_0 {gui_cascade_counter0} {0}
set_instance_parameter_value iopll_0 {gui_cascade_counter1} {0}

set_instance_parameter_value iopll_0 {gui_cascade_outclk_index} {0}
set_instance_parameter_value iopll_0 {gui_clk_bad} {0}
set_instance_parameter_value iopll_0 {gui_clock_name_global} {0}
set_instance_parameter_value iopll_0 {gui_clock_name_string0} {outclk0}
set_instance_parameter_value iopll_0 {gui_clock_name_string1} {outclk1}
set_instance_parameter_value iopll_0 {gui_clock_name_string2} {outclk2}
set_instance_parameter_value iopll_0 {gui_divide_factor_c0} {6}
set_instance_parameter_value iopll_0 {gui_divide_factor_c1} {6}
set_instance_parameter_value iopll_0 {gui_divide_factor_n} {1}
set_instance_parameter_value iopll_0 {gui_dps_cntr} {C0}
set_instance_parameter_value iopll_0 {gui_dps_dir} {Positive}
set_instance_parameter_value iopll_0 {gui_dps_num} {1}
set_instance_parameter_value iopll_0 {gui_dsm_out_sel} {1st_order}
set_instance_parameter_value iopll_0 {gui_duty_cycle0} {50.0}
set_instance_parameter_value iopll_0 {gui_duty_cycle1} {50.0}
set_instance_parameter_value iopll_0 {gui_en_adv_params} {0}
set_instance_parameter_value iopll_0 {gui_en_dps_ports} {0}
set_instance_parameter_value iopll_0 {gui_en_extclkout_ports} {0}
set_instance_parameter_value iopll_0 {gui_en_phout_ports} {0}
set_instance_parameter_value iopll_0 {gui_extclkout_0_source} {C0}
set_instance_parameter_value iopll_0 {gui_extclkout_1_source} {C0}
set_instance_parameter_value iopll_0 {gui_feedback_clock} {Global Clock}
set_instance_parameter_value iopll_0 {gui_fix_vco_frequency} {0}
set_instance_parameter_value iopll_0 {gui_fixed_vco_frequency} {600.0}
set_instance_parameter_value iopll_0 {gui_frac_multiply_factor} {1.0}
set_instance_parameter_value iopll_0 {gui_fractional_cout} {32}
set_instance_parameter_value iopll_0 {gui_multiply_factor} {6}
set_instance_parameter_value iopll_0 {gui_number_of_clocks} {2}
set_instance_parameter_value iopll_0 {gui_operation_mode} {direct}
set_instance_parameter_value iopll_0 {gui_output_clock_frequency0} {2.5}
set_instance_parameter_value iopll_0 {gui_output_clock_frequency1} {25.0}
set_instance_parameter_value iopll_0 {gui_parameter_table_hex_file} {seq_params_sim.hex}
set_instance_parameter_value iopll_0 {gui_phase_shift0} {0.0}
set_instance_parameter_value iopll_0 {gui_phase_shift1} {0.0}
set_instance_parameter_value iopll_0 {gui_phout_division} {1}
set_instance_parameter_value iopll_0 {gui_pll_auto_reset} {0}
set_instance_parameter_value iopll_0 {gui_pll_bandwidth_preset} {Low}
set_instance_parameter_value iopll_0 {gui_pll_freqcal_en} {1}
set_instance_parameter_value iopll_0 {gui_pll_m_cnt_in_src} {c_m_cnt_in_src_ph_mux_clk}
set_instance_parameter_value iopll_0 {gui_pll_mode} {Integer-N PLL}
set_instance_parameter_value iopll_0 {gui_pll_tclk_mux_en} {0}
set_instance_parameter_value iopll_0 {gui_pll_tclk_sel} {pll_tclk_m_src}
set_instance_parameter_value iopll_0 {gui_pll_type} {S10_Simple}
set_instance_parameter_value iopll_0 {gui_pll_vco_freq_band_0} {pll_freq_clk0_disabled}
set_instance_parameter_value iopll_0 {gui_pll_vco_freq_band_1} {pll_freq_clk1_disabled}
set_instance_parameter_value iopll_0 {gui_ps_units0} {ps}
set_instance_parameter_value iopll_0 {gui_ps_units1} {ps}
set_instance_parameter_value iopll_0 {gui_refclk1_frequency} {100.0}
set_instance_parameter_value iopll_0 {gui_refclk_switch} {0}
set_instance_parameter_value iopll_0 {gui_reference_clock_frequency} {100.0}
set_instance_parameter_value iopll_0 {gui_switchover_delay} {0}
set_instance_parameter_value iopll_0 {gui_use_locked} {1}
set_instance_parameter_value iopll_0 {gui_usr_device_speed_grade} {1}
set_instance_parameter_value iopll_0 {gui_vco_frequency} {600.0}
set_instance_parameter_value iopll_0 {hp_qsys_scripting_mode} {0}


set_instance_parameter_value sys_hps {CLK_PERI_PLL_SOURCE2} {0}
set_instance_parameter_value sys_hps {EMAC1_CLK} {250}
set_instance_parameter_value sys_hps {EMAC1_Mode} {RGMII_with_MDIO}
set_instance_parameter_value sys_hps {EMAC1_PTP} {0}
set_instance_parameter_value sys_hps {EMAC1_PinMuxing} {FPGA}
set_instance_parameter_value sys_hps {EMAC1_SWITCH_Enable} {0}
set_instance_parameter_value sys_hps {FPGA_PERIPHERAL_OUTPUT_CLOCK_FREQ_EMAC1_GTX_CLK} {125}
set_instance_parameter_value sys_hps {FPGA_PERIPHERAL_OUTPUT_CLOCK_FREQ_EMAC1_MD_CLK} {2.5}
set_instance_parameter_value sys_hps {EMAC2_CLK} {250}
set_instance_parameter_value sys_hps {EMAC2_Mode} {RGMII_with_MDIO}
set_instance_parameter_value sys_hps {EMAC2_PTP} {0}
set_instance_parameter_value sys_hps {EMAC2_PinMuxing} {FPGA}
set_instance_parameter_value sys_hps {EMAC2_SWITCH_Enable} {0}
set_instance_parameter_value sys_hps {FPGA_PERIPHERAL_OUTPUT_CLOCK_FREQ_EMAC2_GTX_CLK} {125}
set_instance_parameter_value sys_hps {FPGA_PERIPHERAL_OUTPUT_CLOCK_FREQ_EMAC2_MD_CLK} {2.5}
set_instance_parameter_value sys_hps {EMAC_PTP_REF_CLK} {100}
set_instance_parameter_value sys_hps {EMIF_BYPASS_CHECK} {0}
set_instance_parameter_value sys_hps {EMIF_CONDUIT_Enable} {1}


# exported interfaces
add_interface sys_hps_emac1_md_clk clock source
set_interface_property sys_hps_emac1_md_clk EXPORT_OF sys_hps.emac1_md_clk
add_interface sys_hps_emac2_md_clk clock source
set_interface_property sys_hps_emac2_md_clk EXPORT_OF sys_hps.emac2_md_clk
add_interface gmii_to_rgmii_adapter_0_phy_rgmii conduit end
set_interface_property gmii_to_rgmii_adapter_0_phy_rgmii EXPORT_OF gmii_to_rgmii_adapter_0.phy_rgmii
add_interface hps_emac_interface_splitter_0_mdio conduit end
set_interface_property hps_emac_interface_splitter_0_mdio EXPORT_OF hps_emac_interface_splitter_0.mdio
add_interface hps_emac_interface_splitter_0_ptp conduit end
set_interface_property hps_emac_interface_splitter_0_ptp EXPORT_OF hps_emac_interface_splitter_0.ptp
add_interface iopll_0_locked conduit end
set_interface_property iopll_0_locked EXPORT_OF iopll_0.locked

add_interface gmii_to_rgmii_adapter_0_hps_gmii conduit end
set_interface_property gmii_to_rgmii_adapter_0_hps_gmii EXPORT_OF gmii_to_rgmii_adapter_0.hps_gmii
add_interface hps_emac_interface_splitter_0_hps_gmii conduit end
set_interface_property hps_emac_interface_splitter_0_hps_gmii EXPORT_OF hps_emac_interface_splitter_0.hps_gmii

add_interface gmii_to_rgmii_adapter_1_hps_gmii conduit end
set_interface_property gmii_to_rgmii_adapter_1_hps_gmii EXPORT_OF gmii_to_rgmii_adapter_1.hps_gmii
add_interface hps_emac_interface_splitter_1_hps_gmii conduit end
set_interface_property hps_emac_interface_splitter_1_hps_gmii EXPORT_OF hps_emac_interface_splitter_1.hps_gmii


add_interface gmii_to_rgmii_adapter_1_phy_rgmii conduit end
set_interface_property gmii_to_rgmii_adapter_1_phy_rgmii EXPORT_OF gmii_to_rgmii_adapter_1.phy_rgmii
add_interface hps_emac_interface_splitter_1_mdio conduit end
set_interface_property hps_emac_interface_splitter_1_mdio EXPORT_OF hps_emac_interface_splitter_1.mdio
add_interface hps_emac_interface_splitter_1_ptp conduit end
set_interface_property hps_emac_interface_splitter_1_ptp EXPORT_OF hps_emac_interface_splitter_1.ptp

add_connection hps_emac_interface_splitter_0.emac sys_hps.emac1
set_connection_parameter_value hps_emac_interface_splitter_0.emac/sys_hps.emac1 endPort {}
set_connection_parameter_value hps_emac_interface_splitter_0.emac/sys_hps.emac1 endPortLSB {0}
set_connection_parameter_value hps_emac_interface_splitter_0.emac/sys_hps.emac1 startPort {}
set_connection_parameter_value hps_emac_interface_splitter_0.emac/sys_hps.emac1 startPortLSB {0}
set_connection_parameter_value hps_emac_interface_splitter_0.emac/sys_hps.emac1 width {0}

add_connection hps_emac_interface_splitter_0.emac_rx_clk_in sys_hps.emac1_rx_clk_in
add_connection hps_emac_interface_splitter_0.emac_tx_clk_in sys_hps.emac1_tx_clk_in

add_connection iopll_0.outclk0 gmii_to_rgmii_adapter_0.pll_2_5m_clock
add_connection iopll_0.outclk1 gmii_to_rgmii_adapter_0.pll_25m_clock

add_connection sys_clk.clk gmii_to_rgmii_adapter_0.peri_clock
add_connection sys_clk.clk_reset gmii_to_rgmii_adapter_0.peri_reset

add_connection sys_clk.clk iopll_0.refclk
add_connection sys_clk.clk_reset iopll_0.reset

add_connection sys_clk.clk sys_hps.emac_ptp_ref_clock
add_connection sys_hps.emac1_gtx_clk hps_emac_interface_splitter_0.emac_gtx_clk
add_connection sys_hps.emac1_rx_reset hps_emac_interface_splitter_0.emac_rx_reset
add_connection sys_hps.emac1_tx_reset hps_emac_interface_splitter_0.emac_tx_reset

add_connection hps_emac_interface_splitter_1.emac sys_hps.emac2
set_connection_parameter_value hps_emac_interface_splitter_1.emac/sys_hps.emac2 endPort {}
set_connection_parameter_value hps_emac_interface_splitter_1.emac/sys_hps.emac2 endPortLSB {0}
set_connection_parameter_value hps_emac_interface_splitter_1.emac/sys_hps.emac2 startPort {}
set_connection_parameter_value hps_emac_interface_splitter_1.emac/sys_hps.emac2 startPortLSB {0}
set_connection_parameter_value hps_emac_interface_splitter_1.emac/sys_hps.emac2 width {0}

add_connection hps_emac_interface_splitter_1.emac_rx_clk_in sys_hps.emac2_rx_clk_in
add_connection hps_emac_interface_splitter_1.emac_tx_clk_in sys_hps.emac2_tx_clk_in

add_connection iopll_0.outclk0 gmii_to_rgmii_adapter_1.pll_2_5m_clock
add_connection iopll_0.outclk1 gmii_to_rgmii_adapter_1.pll_25m_clock

add_connection sys_clk.clk gmii_to_rgmii_adapter_1.peri_clock
add_connection sys_clk.clk_reset gmii_to_rgmii_adapter_1.peri_reset

add_connection sys_hps.emac2_gtx_clk hps_emac_interface_splitter_1.emac_gtx_clk
add_connection sys_hps.emac2_rx_reset hps_emac_interface_splitter_1.emac_rx_reset
add_connection sys_hps.emac2_tx_reset hps_emac_interface_splitter_1.emac_tx_reset
