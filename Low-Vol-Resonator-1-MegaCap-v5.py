import numpy as np
import gds_geometry_evaluator as gds

inductor_spec = gds.DoubleMeanderSpec(
    trace_width_microns=4.0,
    gap_width_microns=4.0,
    bounding_box_width_microns=284.0,
    bounding_box_height_microns=250.0,
    meander_inner_gap_width_microns=4.0,
    # target_number_of_squares=11000.0,
    layer=1,
)
inductor_built = gds.build_double_meander(inductor_spec)
inductor_built.plot()

# inductor_eval = gds.evaluate_generated_double_meander(inductor_spec, save_path=None, film_thickness_nanometers=30.0)
# print(inductor_eval)

idc_spec = gds.IdcSpec(
    finger_count=42,
    finger_trace_width_microns=5.0,
    # finger_length_microns=950.0,
    finger_gap_width_microns=5.0,
    arm_trace_width_microns=80.0,
    arm_gap_width_microns=10.0,
    bounding_box_width_microns=1695.0,
    final_finger_length_fraction=1.0,
    include_bottom_bars=True,
    omit_top_arm_stubs=True,
    layer=2,
)
idc_built = gds.build_idc(idc_spec)
idc_built.plot()

# idc_eval = gds.evaluate_generated_idc(idc_spec, save_path=None, effective_permittivity=9.08)
# print(idc_eval)

gs_trace_width = 20.0
gs_gap_width = 20.0

ground_shield_spec = gds.GroundShieldSpec(
    trace_thickness_microns=gs_trace_width,
    horizontal_gap_microns=gs_gap_width,
    upper_gap_microns=gs_gap_width,
    lower_gap_microns=gs_gap_width,
)

built_lekid = gds.build_double_meander_with_idc(
                        inductor_spec=inductor_spec,
                        idc_spec=idc_spec,
                        ground_shield_spec=ground_shield_spec,
                        )

built_lekid.plot()

# lekid_eval = gds.evaluate_generated_double_meander_with_idc(built_lekid, 
#                                                effective_permittivity=9.08, 
#                                                kinetic_inductance_per_square_nh=0.0, 
#                                                film_thickness_nanometers=30.0
#                                               )

# print(lekid_eval)

cpw_gap_width = 10.75
cpw_gnd_width = 100.0

fl_launch_spec = gds.FeedlineLauncherSpec(
    central_conductor_width_microns=20,
    gap_width_microns=cpw_gap_width,
    ground_conductor_width_microns=cpw_gnd_width,
    signal_bond_pad_edge_width_microns=300,
    ground_bond_pad_edge_width_microns=1500,
    template_path="/home/dtemples/GDS-Geometry-Evaluator/assets/feedlines/feedline-launch-caltech-style.gds",
    layer=3,
    datatype=0,
)

fl_launch_built = gds.build_feedline_launcher(fl_launch_spec)
fl_launch_built.plot()

fl_spec = gds.StraightFeedlineSpec(
    launcher_spec=fl_launch_spec,
    chip_width_microns=3500,
    chip_height_microns=4000,
    face="left",
    offset_microns=0,
)

built_fl = gds.build_straight_feedline(fl_spec)
built_fl.plot()

placed = gds.place_lekid_on_feedline(
        feedline_result=built_fl,
        lekid_result=built_lekid,
        spec=gds.LekidFeedlinePlacementSpec(
            separation_microns=1.0*(cpw_gap_width+cpw_gnd_width+gs_gap_width),
            position_microns=0.0,
        )
    )


gds.write_built_gds("./Low-Vol-Resonator-1-MegaCap-v5.gds", placed)
