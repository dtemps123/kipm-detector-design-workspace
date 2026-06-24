import matplotlib.pyplot as plt

import gds_geometry_evaluator as gds

# from build_resonator_GRresolve_var3 import build_resonator as build_res
from build_resonator_MLA5G_var2 import build_resonator as build_res


CPW_params = {
    "sig_width": 20.0,
    "gap_width": 10.75,
    "gnd_width": 100.0,
    "sig_bond_width": 300.0,
    "gnd_bond_width": 1500.0,
    "style": "Caltech"
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
            "/home/dtemples/GDS-Geometry-Evaluator/assets/feedlines/feedline-launch-caltech-style.gds" if CPW_params["style"].lower()=='caltech' else
            "/home/dtemples/GDS-Geometry-Evaluator/assets/feedlines/feedline-launch-COH_SQMS-v2-style-positive.gds"
            ),
    )
    fl_launch_built = gds.build_feedline_launcher(fl_launch_spec)

    ## Define and build the feedline
    fl_spec = gds.StraightFeedlineSpec(
        launcher_spec=fl_launch_spec,
        chip_width_microns=4500,
        chip_height_microns=4500,
        face="left",
        offset_microns=0,
    )
    built_fl = gds.build_straight_feedline(fl_spec)

    res_offset_um = [-8000, -4000, 0, 4000, 8000]

    placed = gds.place_lekid_on_feedline(
                feedline_result=built_fl,
                lekid_result=build_res(),
                spec=gds.LekidFeedlinePlacementSpec(
                    separation_microns=CPW_params["gap_width"]+CPW_params["gnd_width"]+20.0,
                    position_microns=0.0,
                    row_index=0,
                )
            )

    return placed


if __name__ == "__main__":

    built_device = build_device()
    gds.write_built_gds("./MLA5G_var2_testgeom.gds", built_device)
    built_device.plot()