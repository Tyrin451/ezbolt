import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


def preview(boltgroup, ax=None):
    """
    Preview bolt configuration
    """   

    if ax is None:
        fig, axs = plt.subplots(1,2, gridspec_kw={"width_ratios":[2,3]}, figsize=(11,8.5))
        plot_ax = axs[1]
        info_ax = axs[0]
        fig.suptitle("Bolt Group Preview", fontweight="bold", fontsize=16)
        apply_tight_layout = True
    else:
        fig = ax.figure
        plot_ax = ax
        info_ax = None
        apply_tight_layout = False

    # plot bolts
    for bolt in boltgroup.bolts :
        plot_ax.plot([bolt.x],[bolt.y],
                 marker="h",
                 markerfacecolor="lightgrey",
                 markeredgecolor="black",
                 markeredgewidth=3,
                 markersize=16,
                 zorder=2,
                 linestyle="none")
        plot_ax.annotate("{}".format(bolt.tag),
                     xy=(bolt.x, bolt.y), 
                     xycoords='data', 
                     xytext=(6, 9), 
                     textcoords='offset points', 
                     fontsize=20,
                     ha = "left",
                     va = "bottom",
                     c = "black")
        
    # plot Cog
    plot_ax.plot(boltgroup.x_cg, boltgroup.y_cg, marker="X",c="red",markersize=6,zorder=2,linestyle="none")
    
    if info_ax:
        # annotation for bolt group properties
        xo = 0.12
        yo = 0.65
        dy = 0.045
        info_ax.annotate("Bolt Group Properties",
                        (xo-0.03,yo), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$N_{{bolts}} = {:.0f}$".format(boltgroup.N_bolt),
                        (xo,yo-dy*1), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$x_{{cg}} = {:.1f} \quad in$".format(boltgroup.x_cg),
                        (xo,yo-dy*2), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$y_{{cg}} = {:.1f} \quad in$".format(boltgroup.y_cg),
                        (xo,yo-dy*3), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{x}} = {:.1f} \quad in^3$".format(boltgroup.Ix),
                        (xo,yo-dy*4), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{y}} = {:.1f} \quad in^3$".format(boltgroup.Iy),
                        (xo,yo-dy*5), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$J = {:.1f} \quad in^3$".format(boltgroup.Iz),
                        (xo,yo-dy*6), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.set_xticks([])
        info_ax.set_yticks([])
    
    # styling
    plot_ax.grid()
    plot_ax.set_axisbelow(True)
    plot_ax.grid(linestyle='--')

    if apply_tight_layout:
        plt.tight_layout()
    
    
    # set axis limit, first use auto, then expand by 10% to not clip annotations
    plot_ax.set_aspect('equal', 'datalim')
    x_min, x_max = plot_ax.get_xlim()
    y_min, y_max = plot_ax.get_ylim()
    x_length = x_max - x_min
    y_length = y_max - y_min
    plot_ax.set_xlim(x_min - 0.1*x_length, x_max + 0.1*x_length)
    plot_ax.set_ylim(y_min - 0.1*y_length, y_max + 0.1*y_length)
    
    return fig


def plot_elastic(boltgroup, annotate_force=True, ax=None):
    """
    Plot bolt forces from elastic method
    """
    if ax is None:
        fig, axs = plt.subplots(1,2, gridspec_kw={"width_ratios":[2,3]}, figsize=[11,8.5])
        plot_ax = axs[1]
        info_ax = axs[0]
        fig.suptitle("Elastic Method - Superposition", fontweight="bold", fontsize=16)
        apply_tight_layout = True
    else:
        fig = ax.figure
        plot_ax = ax
        info_ax = None
        apply_tight_layout = False

    # arrow size scaling set up. 
    # Larrow_max is set to 20% of x and y bound. Qarrow_max the associated amplitude. 
    # Therefore, L = (q/Qarrow_max) * Larrow_max
    ybound = max([b.y for b in boltgroup.bolts]) - min([b.y for b in boltgroup.bolts])
    xbound = max([b.x for b in boltgroup.bolts]) - min([b.x for b in boltgroup.bolts])
    Larrow_max = max(xbound,ybound) * 0.20
    Qarrow_max = max([b.v_resultant for b in boltgroup.bolts]) if boltgroup.bolts else 0
    ARROWWIDTH = 0.03
    
    if info_ax:
        # text box showing applied load
        xo = 0.12
        yo = 0.85
        dy = 0.045
        info_ax.annotate("Bolt Group Properties",
                        (xo-0.03,yo), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$N_{{bolts}} = {:.0f}$".format(boltgroup.N_bolt),
                        (xo,yo-dy*1), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$x_{{cg}} = {:.1f} \quad in$".format(boltgroup.x_cg),
                        (xo,yo-dy*2), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$y_{{cg}} = {:.1f} \quad in$".format(boltgroup.y_cg),
                        (xo,yo-dy*3), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{x}} = {:.1f} \quad in^3$".format(boltgroup.Ix),
                        (xo,yo-dy*4), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{y}} = {:.1f} \quad in^3$".format(boltgroup.Iy),
                        (xo,yo-dy*5), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$J = {:.1f} \quad in^3$".format(boltgroup.Iz),
                        (xo,yo-dy*6), xycoords='axes fraction', fontsize=14, va="top", ha="left")

        info_ax.annotate("Applied Loading",
                        (xo-0.03,yo-dy*7), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$V_x = {:.1f} \quad kips$".format(boltgroup.Vx),
                        (xo,yo-dy*8), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$V_y = {:.1f} \quad kips$".format(boltgroup.Vy),
                        (xo,yo-dy*9), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$M_z = {:.1f} \quad k.in$".format(boltgroup.torsion),
                        (xo,yo-dy*10), xycoords='axes fraction', fontsize=14, va="top", ha="left")

        info_ax.annotate("Results",
                        (xo-0.03,yo-dy*11), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"Bolt Demand = {:.2f} kips".format(boltgroup.bolt_demand),
                        (xo,yo-dy*12), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"Bolt Capacity = {:.2f} kips".format(boltgroup.bolt_capacity),
                        (xo,yo-dy*13), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"D/C ratio = {:.2f}".format(boltgroup.bolt_demand / boltgroup.bolt_capacity),
                        (xo,yo-dy*14), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.set_xticks([])
        info_ax.set_yticks([])
    
    # plot bolts
    for bolt in boltgroup.bolts:
        plot_ax.plot([bolt.x],[bolt.y],
                 marker="h",
                 markerfacecolor="lightgray",
                 markeredgecolor="black",
                 markeredgewidth=2,
                 markersize=16,
                 zorder=2,
                 linestyle="none")
        if annotate_force:
            plot_ax.annotate("({:.1f} k, {:.1f} k)".format(bolt.vx_total, bolt.vy_total),
                         xy=(bolt.x, bolt.y), 
                         xycoords='data', 
                         xytext=(0, -16), 
                         textcoords='offset points', 
                         fontsize=10, 
                         c="black", 
                         ha="center",
                         va="top",
                         zorder=1,
                         bbox=dict(boxstyle='round', facecolor='white'))
        
    # plot Cog
    plot_ax.plot(boltgroup.x_cg, boltgroup.y_cg, marker="X",c="red",markersize=6,zorder=2,linestyle="none")

    if Qarrow_max > 0:
        # bolts reaction arrows
        for bolt in boltgroup.bolts:
            L_arrow = (bolt.v_resultant / Qarrow_max) * Larrow_max
            dx_arrow = L_arrow * math.cos(math.radians(bolt.theta))
            dy_arrow = L_arrow * math.sin(math.radians(bolt.theta))
            plot_ax.arrow(bolt.x,
                    bolt.y,
                    dx_arrow,
                    dy_arrow,
                    width=ARROWWIDTH,
                    head_width=8*ARROWWIDTH,
                    head_length=8*ARROWWIDTH,
                    fc='black',
                    ec='black',
                    zorder=2)
    
    # applied force arrows
    if boltgroup.V_resultant != 0:
        L_arrow = Larrow_max * 1.4 if Qarrow_max > 0 else max(xbound,ybound) * 0.20 * 1.4
        dx_arrow = L_arrow * math.cos(math.radians(boltgroup.theta))
        dy_arrow = L_arrow * math.sin(math.radians(boltgroup.theta))
        x_arrow = boltgroup.x_cg
        y_arrow = boltgroup.y_cg
        plot_ax.arrow(x_arrow-dx_arrow,
                  y_arrow-dy_arrow, 
                  dx_arrow, 
                  dy_arrow, 
                  width=ARROWWIDTH,
                  head_width=8*ARROWWIDTH, 
                  head_length=8*ARROWWIDTH,
                  fc='red', 
                  ec='red', 
                  zorder=3,
                  head_starts_at_zero=False,
                  length_includes_head=True)
        
    if boltgroup.torsion != 0:
        style = "Simple, tail_width=0.8, head_width=10, head_length=10"
        rotation_sign = -1.0 if boltgroup.torsion < 0 else 1.0
        moment_arrow = patches.FancyArrowPatch((boltgroup.x_cg+rotation_sign*0.6, boltgroup.y_cg),
                                               (boltgroup.x_cg-rotation_sign*0.6, boltgroup.y_cg),
                                               connectionstyle=f"arc3,rad={0.65*rotation_sign}",
                                               arrowstyle = style,
                                               color="red")
        plot_ax.add_patch(moment_arrow)
        
    # styling
    plot_ax.grid()
    plot_ax.set_axisbelow(True)
    plot_ax.grid(linestyle='--')
    
    # set axis limit, first use auto, then expand by 10% to not clip annotations
    plot_ax.set_aspect('equal', 'datalim')
    x_min, x_max = plot_ax.get_xlim()
    y_min, y_max = plot_ax.get_ylim()
    x_length = x_max - x_min
    y_length = y_max - y_min
    plot_ax.set_xlim(x_min - 0.2*x_length, x_max + 0.2*x_length)
    plot_ax.set_ylim(y_min - 0.2*y_length, y_max + 0.2*y_length)
    
    if apply_tight_layout:
        plt.tight_layout()

    return fig


def plot_ECR(boltgroup, annotate_force=True, ax=None):
    """
    plot bolt forces from ECR method.
    """
    if ax is None:
        if boltgroup.torsion == 0:
            fig, ax = plt.subplots()
            ax.annotate("ECR method is not applicable for torsion = 0",
                         xy=(0,0),
                         xytext=(0.05,0.5),
                         textcoords='axes fraction',
                         fontsize=14)
            return fig

        fig, axs = plt.subplots(1,2, gridspec_kw={"width_ratios":[2,3]}, figsize=[11,8.5])
        plot_ax = axs[1]
        info_ax = axs[0]
        fig.suptitle("Elastic Method - Center of Rotation", fontweight="bold", fontsize=16)
        apply_tight_layout = True
    else:
        fig = ax.figure
        plot_ax = ax
        info_ax = None
        apply_tight_layout = False
        if boltgroup.torsion == 0:
            plot_ax.clear()
            plot_ax.annotate("ECR method is not applicable for torsion = 0",
                            xy=(0,0),
                            xytext=(0.05,0.5),
                            textcoords='axes fraction',
                            fontsize=14)
            return fig

    # arrow size scaling set up. 
    # Larrow_max is set to 20% of x and y bound. Qarrow_max the associated amplitude. 
    # Therefore, L = (q/Qarrow_max) * Larrow_max
    ybound = max([b.y for b in boltgroup.bolts]) - min([b.y for b in boltgroup.bolts])
    xbound = max([b.x for b in boltgroup.bolts]) - min([b.x for b in boltgroup.bolts])
    Larrow_max = max(xbound,ybound) * 0.20
    Qarrow_max = max([b.vtotal_ECR for b in boltgroup.bolts]) if boltgroup.bolts else 0
    ARROWWIDTH = 0.03
    
    if info_ax:
        # text box showing applied load
        xo = 0.12
        yo = 0.95
        dy = 0.045
        unit = "kips" if boltgroup.ecc!=0 else "k.in"
        info_ax.annotate("Bolt Group Properties",
                        (xo-0.03,yo), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$N_{{bolts}} = {:.0f}$".format(boltgroup.N_bolt),
                        (xo,yo-dy*1), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$x_{{cg}} = {:.1f} \quad in$".format(boltgroup.x_cg),
                        (xo,yo-dy*2), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$y_{{cg}} = {:.1f} \quad in$".format(boltgroup.y_cg),
                        (xo,yo-dy*3), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{x}} = {:.1f} \quad in^3$".format(boltgroup.Ix),
                        (xo,yo-dy*4), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{y}} = {:.1f} \quad in^3$".format(boltgroup.Iy),
                        (xo,yo-dy*5), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$J = {:.1f} \quad in^3$".format(boltgroup.Iz),
                        (xo,yo-dy*6), xycoords='axes fraction', fontsize=14, va="top", ha="left")

        info_ax.annotate("Applied Loading",
                        (xo-0.03,yo-dy*7), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$V_x = {:.1f} \quad kips$".format(boltgroup.Vx),
                        (xo,yo-dy*8), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$V_y = {:.1f} \quad kips$".format(boltgroup.Vy),
                        (xo,yo-dy*9), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$M_z = {:.1f} \quad k.in$".format(boltgroup.torsion),
                        (xo,yo-dy*10), xycoords='axes fraction', fontsize=14, va="top", ha="left")

        info_ax.annotate("Results",
                        (xo-0.03,yo-dy*11), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$ECR = ({:.2f}, {:.2f})$".format(boltgroup.ECR_x, boltgroup.ECR_y),
                        (xo,yo-dy*12), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$C_e = {:.2f}$".format(boltgroup.Ce),
                        (xo,yo-dy*13), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"Connection Capacity = {:.2f} {}".format(boltgroup.P_capacity, unit),
                        (xo,yo-dy*14), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"Connection Demand = {:.2f} {}".format(boltgroup.P_demand, unit),
                        (xo,yo-dy*15), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"D/C Ratio = {:.2f}".format(boltgroup.P_demand / boltgroup.P_capacity),
                        (xo,yo-dy*16), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.set_xticks([])
        info_ax.set_yticks([])

    # plot bolts
    for bolt in boltgroup.bolts:
        plot_ax.plot([bolt.x],[bolt.y],
                 marker="h",
                 markerfacecolor="lightgray",
                 markeredgecolor="black",
                 markeredgewidth=2,
                 markersize=16,
                 zorder=2,
                 linestyle="none")
        if annotate_force:
            plot_ax.annotate("({:.1f} k, {:.1f} k)".format(bolt.vx_ECR, bolt.vy_ECR),
                         xy=(bolt.x, bolt.y), 
                         xycoords='data', 
                         xytext=(0, -16), 
                         textcoords='offset points', 
                         fontsize=10, 
                         c="black", 
                         ha="center",
                         va="top",
                         zorder=1,
                         bbox=dict(boxstyle='round', facecolor='white'))
    # plot Cog
    plot_ax.plot(boltgroup.x_cg, boltgroup.y_cg, marker="X",c="red",markersize=6,zorder=2,linestyle="none")

    # plot ECR
    if boltgroup.torsion != 0:
        plot_ax.plot(boltgroup.ECR_x, boltgroup.ECR_y, marker="*",c="red",markersize=14,zorder=3,linestyle="none")
    
    if Qarrow_max > 0:
        # bolts reaction arrows
        for bolt in boltgroup.bolts:
            L_arrow = (bolt.vtotal_ECR / Qarrow_max) * Larrow_max
            dx_arrow = L_arrow * math.cos(math.radians(bolt.theta_ECR))
            dy_arrow = L_arrow * math.sin(math.radians(bolt.theta_ECR))
            plot_ax.arrow(bolt.x,
                    bolt.y,
                    dx_arrow,
                    dy_arrow,
                    width=ARROWWIDTH,
                    head_width=8*ARROWWIDTH,
                    head_length=8*ARROWWIDTH,
                    fc='black',
                    ec='black',
                    zorder=2)
    
    # applied force arrows
    if boltgroup.V_resultant != 0:
        L_arrow = Larrow_max * 1.4 if Qarrow_max > 0 else max(xbound,ybound) * 0.20 * 1.4
        dx_arrow = L_arrow * math.cos(math.radians(boltgroup.theta))
        dy_arrow = L_arrow * math.sin(math.radians(boltgroup.theta))
        x_arrow = boltgroup.x_cg + boltgroup.ecc_x
        y_arrow = boltgroup.y_cg + boltgroup.ecc_y
        plot_ax.axline([x_arrow-dx_arrow, y_arrow-dy_arrow],
                      [x_arrow, y_arrow],
                      linewidth=1,
                      linestyle="--",
                      color="black")
        plot_ax.axline([x_arrow, y_arrow],
                      [boltgroup.x_cg, boltgroup.y_cg],
                      linewidth=1,
                      linestyle="--",
                      color="black")
        plot_ax.arrow(x_arrow-dx_arrow,
                  y_arrow-dy_arrow, 
                  dx_arrow, 
                  dy_arrow, 
                  width=ARROWWIDTH,
                  head_width=8*ARROWWIDTH, 
                  head_length=8*ARROWWIDTH,
                  fc='red', 
                  ec='red', 
                  zorder=3,
                  head_starts_at_zero=False,
                  length_includes_head=True)
        
    # styling
    plot_ax.grid()
    plot_ax.set_axisbelow(True)
    plot_ax.grid(linestyle='--')
    
    # set axis limit, first use auto, then expand by 10% to not clip annotations
    plot_ax.set_aspect('equal', 'datalim')
    x_min, x_max = plot_ax.get_xlim()
    y_min, y_max = plot_ax.get_ylim()
    x_length = x_max - x_min
    y_length = y_max - y_min
    plot_ax.set_xlim(x_min - 0.3*x_length, x_max + 0.3*x_length)
    plot_ax.set_ylim(y_min - 0.3*y_length, y_max + 0.3*y_length)
    
    if apply_tight_layout:
        plt.tight_layout()
    
    return fig


def plot_ICR(boltgroup, annotate_force=True, ax=None):
    """
    plot bolt forces from ICR method.
    """
    if ax is None:
        if boltgroup.torsion == 0:
            fig, ax = plt.subplots()
            ax.annotate("ICR method is not applicable for torsion = 0",
                         xy=(0,0),
                         xytext=(0.05,0.5),
                         textcoords='axes fraction',
                         fontsize=14)
            return fig

        fig, axs = plt.subplots(1,2, gridspec_kw={"width_ratios":[2,3]}, figsize=[11,8.5])
        plot_ax = axs[1]
        info_ax = axs[0]
        fig.suptitle("Instant Center of Rotation Method", fontweight="bold", fontsize=16)
        apply_tight_layout = True
    else:
        fig = ax.figure
        plot_ax = ax
        info_ax = None
        apply_tight_layout = False
        if boltgroup.torsion == 0:
            plot_ax.clear()
            plot_ax.annotate("ICR method is not applicable for torsion = 0",
                            xy=(0,0),
                            xytext=(0.05,0.5),
                            textcoords='axes fraction',
                            fontsize=14)
            return fig

    # arrow size scaling set up. 
    # Larrow_max is set to 20% of x and y bound. Qarrow_max the associated amplitude. 
    # Therefore, L = (q/Qarrow_max) * Larrow_max
    ybound = max([b.y for b in boltgroup.bolts]) - min([b.y for b in boltgroup.bolts])
    xbound = max([b.x for b in boltgroup.bolts]) - min([b.x for b in boltgroup.bolts])
    Larrow_max = max(xbound,ybound) * 0.20
    Qarrow_max = max([abs(b.force_ICR[-1]) for b in boltgroup.bolts]) if boltgroup.bolts else 0
    #Qarrow_max = boltgroup.V_resultant
    ARROWWIDTH = 0.03
    
    if info_ax:
        # text box showing applied load
        xo = 0.12
        yo = 0.95
        dy = 0.045
        unit = "kips" if boltgroup.ecc!=0 else "k.in"
        info_ax.annotate("Bolt Group Properties",
                        (xo-0.03,yo), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$N_{{bolts}} = {:.0f}$".format(boltgroup.N_bolt),
                        (xo,yo-dy*1), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$x_{{cg}} = {:.1f} \quad in$".format(boltgroup.x_cg),
                        (xo,yo-dy*2), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$y_{{cg}} = {:.1f} \quad in$".format(boltgroup.y_cg),
                        (xo,yo-dy*3), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{x}} = {:.1f} \quad in^3$".format(boltgroup.Ix),
                        (xo,yo-dy*4), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$I_{{y}} = {:.1f} \quad in^3$".format(boltgroup.Iy),
                        (xo,yo-dy*5), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$J = {:.1f} \quad in^3$".format(boltgroup.Iz),
                        (xo,yo-dy*6), xycoords='axes fraction', fontsize=14, va="top", ha="left")

        info_ax.annotate("Applied Loading",
                        (xo-0.03,yo-dy*7), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$P = {:.1f} \quad kips$".format(boltgroup.V_resultant),
                        (xo,yo-dy*8), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$\theta = {:.1f} \quad degs$".format(boltgroup.theta),
                        (xo,yo-dy*9), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$e_x = {:.2f} \quad in$".format(boltgroup.ecc_x),
                        (xo,yo-dy*10), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$e_y = {:.2f} \quad in$".format(boltgroup.ecc_y),
                        (xo,yo-dy*11), xycoords='axes fraction', fontsize=14, va="top", ha="left")

        info_ax.annotate("Results",
                        (xo-0.03,yo-dy*12), fontweight="bold",xycoords='axes fraction', fontsize=12, va="top", ha="left")
        info_ax.annotate(r"$ICR = ({:.2f}, {:.2f})$".format(boltgroup.ICR_x[-1], boltgroup.ICR_y[-1]),
                        (xo,yo-dy*13), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"$C_u = {:.2f}$".format(boltgroup.Cu[-1]),
                        (xo,yo-dy*14), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"Connection Capacity = {:.2f} {}".format(boltgroup.P_capacity_ICR, unit),
                        (xo,yo-dy*15), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"Connection Demand = {:.2f} {}".format(boltgroup.P_demand_ICR, unit),
                        (xo,yo-dy*16), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.annotate(r"D/C Ratio = {:.2f}".format(abs(boltgroup.P_demand_ICR / boltgroup.P_capacity_ICR)),
                        (xo,yo-dy*17), xycoords='axes fraction', fontsize=14, va="top", ha="left")
        info_ax.set_xticks([])
        info_ax.set_yticks([])
    
    # plot bolts
    for bolt in boltgroup.bolts:
        plot_ax.plot([bolt.x],[bolt.y],
                 marker="h",
                 markerfacecolor="lightgray",
                 markeredgecolor="black",
                 markeredgewidth=2,
                 markersize=16,
                 zorder=2,
                 linestyle="none")
        if annotate_force:
            plot_ax.annotate("({:.1f} k, {:.1f} k)".format(bolt.vx_ICR[-1], bolt.vy_ICR[-1]),
                         xy=(bolt.x, bolt.y), 
                         xycoords='data', 
                         xytext=(0, -16), 
                         textcoords='offset points', 
                         fontsize=10, 
                         c="black", 
                         ha="center",
                         va="top",
                         zorder=1,
                         bbox=dict(boxstyle='round', facecolor='white'))
    # plot Cog
    plot_ax.plot(boltgroup.x_cg, boltgroup.y_cg, marker="X",c="darkblue",markersize=6,zorder=2,linestyle="none")

    # plot ICR
    if boltgroup.torsion != 0:
        plot_ax.plot(boltgroup.ICR_x[-1], boltgroup.ICR_y[-1], marker="*",c="red",markersize=14,zorder=3,linestyle="none")
        # axs[1].annotate("ICR",
        #              xy=(boltgroup.ICR_x[-1], boltgroup.ICR_y[-1]), xycoords='data', color="red",
        #              xytext=(-5, -5), textcoords='offset points', fontsize=16, va="top", ha="right")
    
    if Qarrow_max > 0:
        # bolts reaction arrows
        for bolt in boltgroup.bolts:
            L_arrow = (abs(bolt.force_ICR[-1]) / Qarrow_max) * Larrow_max
            dx_arrow = L_arrow * math.cos(math.radians(bolt.theta_ICR[-1]))
            dy_arrow = L_arrow * math.sin(math.radians(bolt.theta_ICR[-1]))
            plot_ax.arrow(bolt.x,
                    bolt.y,
                    dx_arrow,
                    dy_arrow,
                    width=ARROWWIDTH,
                    head_width=8*ARROWWIDTH,
                    head_length=8*ARROWWIDTH,
                    fc='black',
                    ec='black',
                    zorder=2)
    
    # applied force arrows
    if boltgroup.V_resultant != 0:
        L_arrow = Larrow_max * 1.4 if Qarrow_max > 0 else max(xbound,ybound) * 0.20 * 1.4
        dx_arrow = L_arrow * math.cos(math.radians(boltgroup.theta))
        dy_arrow = L_arrow * math.sin(math.radians(boltgroup.theta))
        x_arrow = boltgroup.x_cg + boltgroup.ecc_x
        y_arrow = boltgroup.y_cg + boltgroup.ecc_y
        plot_ax.axline([x_arrow-dx_arrow, y_arrow-dy_arrow],
                      [x_arrow, y_arrow],
                      linewidth=1,
                      linestyle="--",
                      color="black")
        plot_ax.axline([x_arrow, y_arrow],
                      [boltgroup.x_cg, boltgroup.y_cg],
                      linewidth=1,
                      linestyle="--",
                      color="black")
        plot_ax.arrow(x_arrow-dx_arrow,
                  y_arrow-dy_arrow, 
                  dx_arrow, 
                  dy_arrow, 
                  width=ARROWWIDTH,
                  head_width=8*ARROWWIDTH, 
                  head_length=8*ARROWWIDTH,
                  fc='red', 
                  ec='red', 
                  zorder=3,
                  head_starts_at_zero=False,
                  length_includes_head=True)
        
    # styling
    plot_ax.grid()
    plot_ax.set_axisbelow(True)
    plot_ax.grid(linestyle='--')
    
    # set axis limit, first use auto, then expand by 10% to not clip annotations
    plot_ax.set_aspect('equal', 'datalim')
    x_min, x_max = plot_ax.get_xlim()
    y_min, y_max = plot_ax.get_ylim()
    x_length = x_max - x_min
    y_length = y_max - y_min
    plot_ax.set_xlim(x_min - 0.3*x_length, x_max + 0.3*x_length)
    plot_ax.set_ylim(y_min - 0.3*y_length, y_max + 0.3*y_length)
    
    if apply_tight_layout:
        plt.tight_layout()
    
    return fig






def plot_convergence(boltgroup, axs=None):
    """
    function used to debug when solver fails to converge
    """
    if axs is None:
        fig, axs = plt.subplots(4,1,figsize=[8,8],sharex=True)
        fig.suptitle("Brandt's Method Convergence Plot", fontweight="bold", fontsize=16)
        apply_tight_layout = True
    else:
        fig = axs[0].figure
        apply_tight_layout = False

    axs[0].plot(boltgroup.residual)
    axs[1].plot(boltgroup.Cu)
    axs[2].plot(boltgroup.ICR_x)
    axs[3].plot(boltgroup.ICR_y)

    # styling
    axs[0].set_title("residual")
    axs[1].set_title("Cu")
    axs[2].set_title("x")
    axs[3].set_title("y")

    if apply_tight_layout:
        plt.tight_layout()
    
    return fig





