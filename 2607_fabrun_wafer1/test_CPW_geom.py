import gds_geometry_evaluator as gds

CPW_params = {
    "sig_width": 20.0,
    "gap_width": 10.75,
    "gnd_width": 100.0,
    "sig_bond_width": 357.0,
    "gnd_bond_width": 500.0,
    "style": "SQMS", # "Caltech" # 
}

def build_device(params = CPW_params):

    ## Define and build the feedline launchers
    fl_launch_spec = gds.FeedlineLauncherSpec(
        central_conductor_width_microns=CPW_params["sig_width"],
        gap_width_microns=CPW_params["gap_width"],
        ground_conductor_width_microns=CPW_params["gnd_width"],
        signal_bond_pad_edge_width_microns=CPW_params["sig_bond_width"],
        ground_bond_pad_edge_width_microns=CPW_params["gnd_bond_width"],
        template_path=(
            "/Users/dtemples/GDS-Geometry-Evaluator/assets/feedlines/feedline-launch-caltech-style.gds" if CPW_params["style"].lower()=='caltech' else
            "/Users/dtemples/GDS-Geometry-Evaluator/assets/feedlines/feedline-launch-COH_SQMS-v2-style-positive.gds"
            ),
        include_ground_bond_pads=True
    )
    fl_launch_built = gds.build_feedline_launcher(fl_launch_spec)

    ## Define and build the feedline
    fl_spec = gds.StraightFeedlineSpec(
        launcher_spec=fl_launch_spec,
        chip_width_microns=22000,
        chip_height_microns=10000,
        face="left",
        offset_microns=0,
        ground_pour_spec=gds.GroundPourSpec(
            chip_edge_border_microns=25,
            structure_gap_microns=5,
            flux_trap_spec=None,
        ),
    )
    built_fl = gds.build_straight_feedline(fl_spec)

    return built_fl


if __name__ == "__main__":

    built_fl = build_device()
    built_fl.plot()