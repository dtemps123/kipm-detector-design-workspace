import matplotlib.pyplot as plt

import gds_geometry_evaluator as gds

## Nominally at 6 GHz
MLA5G_var1_params = {
    "trace_um":          80.0,
    "gap_um":            10.0,
    "inner_gap_um":      20.0,
    "res_width_um":    1130.0,
    "cap_width_um":    1130.0,
    "ind_height_um":    404.0,
    "cap_trace_um":      20.0,
    "cap_finger_num":     7,
    "cap_finger_gap_um": 20.0,
    "cap_arm_width_um":  80.0,
    "cap_arm_gap_um":    10.0,
    "gs_trace_width_um": 80.0,
    "gs_gap_width_um":   20.0,
}

def build_resonator(params=MLA5G_var1_params, return_all_objs=False, ind_ft_spec=None, idc_ft_spec=None, gs_ft_spec=None):

    ## Define and build the inductor
    inductor_spec = gds.DoubleMeanderSpec(
        trace_width_microns=params["trace_um"],
        gap_width_microns=params["gap_um"],
        bounding_box_width_microns=params["res_width_um"],
        bounding_box_height_microns=params["ind_height_um"],
        meander_inner_gap_width_microns=params["inner_gap_um"],
        flux_trap_spec=ind_ft_spec,
    )
    # inductor_built = gds.build_double_meander(inductor_spec)

    ## Define and build the capacitor
    idc_spec = gds.IdcSpec(
        finger_count=params["cap_finger_num"],
        finger_trace_width_microns=params["cap_trace_um"],
        finger_gap_width_microns=params["cap_finger_gap_um"],
        arm_trace_width_microns=params["cap_arm_width_um"],
        arm_gap_width_microns=params["cap_arm_gap_um"],
        bounding_box_width_microns=params["cap_width_um"],
        final_finger_length_fraction=1.0,
        include_bottom_bars=True,
        omit_top_arm_stubs=True,
    )
    # idc_built = gds.build_idc(idc_spec)

    ## Define and built the ground shield
    ground_shield_spec = gds.GroundShieldSpec(
        trace_thickness_microns=params["gs_trace_width_um"],
        horizontal_gap_microns=params["gs_gap_width_um"],
        upper_gap_microns=params["gs_gap_width_um"],
        lower_gap_microns=params["gs_gap_width_um"],
        flux_trap_spec=gs_ft_spec,
    )

    ## Build the whole assembly
    built_lekid = gds.build_double_meander_with_idc(
                            inductor_spec=inductor_spec,
                            idc_spec=idc_spec,
                            ground_shield_spec=ground_shield_spec,
                            idc_flux_trap_spec=idc_ft_spec
                        )

    if return_all_objs:
        return built_lekid, (inductor_spec, idc_spec, ground_shield_spec)
    else:
        return built_lekid


if __name__ == "__main__":

    built_lekid = build_resonator(return_all_objs=False)
    built_lekid.plot()

    lekid_eval = gds.evaluate_generated_double_meander_with_idc(built_lekid, 
                                                   effective_permittivity=9.08, 
                                                   kinetic_inductance_per_square_nh=0.0, 
                                                   film_thickness_nanometers=30.0
                                                  )

    print(lekid_eval)
    plt.show()