import matplotlib.pyplot as plt

import gds_geometry_evaluator as gds

# from build_resonator_GRresolve_var1 import build_resonator as build_GRres_var1
# from build_resonator_GRresolve_var2 import build_resonator as build_GRres_var2
from build_resonator_GRresolve_var3 import build_resonator as build_GRres_var3
from build_resonator_GRresolve_var4 import build_resonator as build_GRres_var4
from build_resonator_MLA5G_narrowtrace_var1 import build_resonator as build_MLA5G_NTvar1
from build_resonator_MLA5G_var1 import build_resonator as build_MLA5G_var1
from build_resonator_MLA5G_var2 import build_resonator as build_MLA5G_var2


CPW_params = {
    "sig_width": 20.0,
    "gap_width": 10.75,
    "gnd_width": 100.0,
    "sig_bond_width": 357.0,
    "gnd_bond_width": 500.0,
    "style": "SQMS", # "Caltech" # 
}

FT_params = {
    "trap_width_um": 5.0,
    "res_trap_pitch_um": 15.0,
    "gp_trap_pitch_um": 150.0,
}

def build_device(params = CPW_params):

    ## Define the flux trap specifications for each object

    ft_for_IDCs = gds.FluxTrapSpec(
        trap_width_microns=FT_params["trap_width_um"], 
        horizontal_separation_microns=FT_params["res_trap_pitch_um"],
        edge_margin_microns=FT_params["trap_width_um"],
    )

    ft_for_GSs = gds.FluxTrapSpec(
        trap_width_microns=FT_params["trap_width_um"],
        horizontal_separation_microns=FT_params["res_trap_pitch_um"],
        edge_margin_microns=FT_params["trap_width_um"],
    )

    ft_for_MIs = gds.FluxTrapSpec(
        trap_width_microns=FT_params["trap_width_um"],
        horizontal_separation_microns=FT_params["res_trap_pitch_um"],
        edge_margin_microns=FT_params["trap_width_um"],
    )

    ft_for_GP = gds.FluxTrapSpec(
        trap_width_microns=20.0, # 10.0 * FT_params["trap_width_um"],
        horizontal_separation_microns=150.0, # FT_params["res_trap_pitch_um"],
        edge_margin_microns=10.0, #30.0 * FT_params["trap_width_um"],
    )

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
            structure_gap_microns=10,
            flux_trap_spec=ft_for_GP,
        ),
        chip_bounds_layer=22,
    )
    built_fl = gds.build_straight_feedline(fl_spec)

    ## Collect all the resonator designs
    all_res = [
        build_GRres_var3(  ind_ft_spec=None,       idc_ft_spec=ft_for_IDCs, gs_ft_spec=ft_for_GSs), ## Mega-Cap at 4.23 GHz
        build_MLA5G_var2(  ind_ft_spec=ft_for_MIs, idc_ft_spec=ft_for_IDCs, gs_ft_spec=ft_for_GSs), ## MLA5G at 4.05 GHz
        build_MLA5G_NTvar1(ind_ft_spec=None,       idc_ft_spec=ft_for_IDCs, gs_ft_spec=ft_for_GSs), ## MLA5G narrow trace at 5.95 GHz
        build_MLA5G_var1(  ind_ft_spec=ft_for_MIs, idc_ft_spec=ft_for_IDCs, gs_ft_spec=ft_for_GSs), ## MLA5G at 6.17 GHz
        build_GRres_var4(  ind_ft_spec=None,       idc_ft_spec=ft_for_IDCs, gs_ft_spec=ft_for_GSs), ## Mega-Cap at 5.42 GHz
    ]

    res_offset_um = [-8000, -4000, 0, 4000, 8000]

    ## Place the LEKIDs on the feedline
    for i,resonator in enumerate(all_res):

        if i==0:   
            placed = gds.place_lekid_on_feedline(
                feedline_result=built_fl,
                lekid_result=resonator,
                spec=gds.LekidFeedlinePlacementSpec(
                    separation_microns=CPW_params["gap_width"]+CPW_params["gnd_width"]+20.0,
                    position_microns=res_offset_um[i],
                    row_index=0,
                )
            )

        else:
            placed = gds.place_lekid_on_feedline(placed,
                lekid_result=resonator,
                spec=gds.LekidFeedlinePlacementSpec(
                    separation_microns=CPW_params["gap_width"]+CPW_params["gnd_width"]+20.0,
                    position_microns=res_offset_um[i],
                    row_index=0,
                )
            )

    return placed


if __name__ == "__main__":

    built_device = build_device()
    built_device.plot()

    gds.write_built_gds("./M20005-DevC2.gds", built_device)
    plt.show()