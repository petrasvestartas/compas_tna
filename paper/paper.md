---
title: 'Gala: A Python package for galactic dynamics'
tags:
  - Python
  - COMPAS
  - form-finding
  - thrust-network-analysis
  - funicular-structures
authors:
  - name: Tom Van Mele
    orcid: 0000-0002-4614-1808
    equal-contrib: true
    affiliation: 1
  - name: Li Chen
    orcid: 0009-0001-1520-9064
    equal-contrib: false
    affiliation: 1
  - name: Juney Lee
    orcid: 0000-0003-4077-0205
    corresponding: false
    affiliation: 2
affiliations:
  - name: Block Research Group (BRG), Institute of Technology in Architecture (ITA), ETH Zürich, Switzerland
    index: 1
    ror: 05a28rw58
  - name: Carnegie Mellon University, United States
    index: 2
    ror: 05x2bcf33
date: 20 August 2025  
bibliography: paper.bib
---

# Summary

Thrust Network Analysis (TNA) is a graphic statics-based method based on COMPAS Python framework for finding the shape of a spatial network of compressive forces in equilibrium with vertical loads applied to its vertices. Traditional approaches to vaulted or shell structures have historically relied on physical models such as hanging chains or cloth experiments, exemplified by the works of Gaudí, Otto, and Isler, or on graphical methods of equilibrium design such as those employed by the Guastavinos. While these methods are powerful for revealing the natural logic of compression-only forms, they are also time-consuming, locally constrained, and lack global control, limiting their application in contemporary design environments. TNA addresses these limitations by explicitly representing equilibrium through a form diagram and its reciprocal force diagram, linked by the spatial thrust network. The designer can manipulate either diagram to steer both form and force, ensuring that equilibrium is maintained while exploring highly indeterminate structural configurations. This bidirectional control over geometry and internal force distribution allows the exploration of vaults with openings, oculi, folds, open-edge arches, or continuous tension ties, which would be cumbersome or even impossible to design with purely numerical or physical methods [@Rippmann2012; @VanMele2012]. What makes TNA particularly significant is its dual emphasis between form and force diagrams \autoref{fig:compas-tna}. The diagrams provide immediate visual feedback about axial forces and equilibrium conditions, while the underlying algorithms enforce structural validity, meaning that the designer’s creative intent is grounded in a precise mathematical framework.

The practical significance of this methodology has been demonstrated through software implementations such as RhinoVAULT, which embed the TNA framework into interactive design tools. These tools provide real-time feedback, enabling designers to intuitively manipulate reciprocal diagrams while observing their spatial consequences in the thrust network. Operations such as local attraction of forces, modification of support conditions, or redistribution of horizontal thrust can be carried out visually and playfully, yet remain structurally sound because the solver continuously enforces equilibrium constraints [@Rippmann2013]. Importantly, the feedback loop between the designer and the computational engine fosters a deeper structural intuition by making the flow of forces transparent: the lengths of edges in the force diagram directly correspond to the magnitudes of axial forces, while closed polygons represent local equilibrium. This makes the relationship between form and force legible to both engineers and architects, allowing them to collaborate effectively during the earliest stages of design. Case studies have validated this approach in both educational and practical contexts. Student workshops using RhinoVAULT have demonstrated how novices can rapidly generate structurally informed vaults and shells, while built prototypes such as full-scale thin-tile vaults or digitally fabricated foam shells confirm that the discovered forms are not only structurally valid but also constructible [@Block2016]. These applications underscore that TNA is more than a numerical solver; it is a design philosophy and visual language for equilibrium that situates geometry at the heart of structural thinking, bridging the conceptual divide between historical craft traditions and contemporary computational design practices.

# Statement of need

Despite the rapid expansion of computational design and finite element analysis (FEA) in architectural practice, early-stage structural form finding remains dominated by either black-box optimization routines or heuristic, trial-and-error modeling, both of which limit the designer’s ability to explore equilibrium structures in a transparent and creative way. Current workflows typically separate the processes of design and analysis: architects model a geometry based on aesthetic considerations, and engineers then evaluate or post-rationalize it using numerical solvers. This division often obscures the crucial relationship between form and force, resulting in designs that either fail to capitalize on the efficiency of funicular geometries or require costly reinforcement strategies. On the other hand, physical methods such as hanging chain models offer immediacy and clarity but are not readily reproducible, globally controllable, or easily integrated into digital workflows. This gap creates a clear need for tools that allow both architects and engineers to simultaneously explore spatial form and structural logic through a common, intuitive language. TNA addresses this need by making equilibrium itself the medium of design. By embedding reciprocal diagrams and thrust networks within interactive software environments, the designer gains real-time, bi-directional control of form and forces, turning what is traditionally a specialist’s analysis into a broadly accessible, exploratory design process [@Rippmann2012; @VanMele2012].

The need for such a framework is particularly acute in the context of education and research. Students in architecture and engineering can struggle to grasp the invisible flow of forces within structures when relying solely on equations or FEA outputs, whereas TNA-based tools make these flows explicit by encoding them in reciprocal geometry. This geometric transparency not only enhances comprehension but also empowers learners to experiment, fail, and iterate rapidly without losing sight of equilibrium constraints. At the research level, the ability to parametrize reciprocal diagrams and link them to optimization routines opens new pathways for generating novel funicular geometries and hybrid compression–tension systems, extending beyond the canonical vault or dome. In practice, the implications are equally significant: the integration of TNA into design workflows provides a lightweight but rigorous front-end for structural conception, complementing downstream finite element checks rather than replacing them. By constraining the design space to admissible equilibrium geometries under vertical loading, the approach ensures that candidate forms are structurally sound from the outset, reducing inefficiencies in iteration between architects and engineers. Moreover, the implementation of TNA in accessible packages such as RhinoVAULT demonstrates that these methods can be disseminated widely as free tools, supporting both professional experimentation and educational adoption. This democratization of structural intuition aligns with the broader movement in computational design towards open, scriptable, and reproducible frameworks. Ultimately, the continued development of TNA-based tools fulfills a pressing need: to bridge the divide between geometry, structure, and fabrication in a way that is both rigorous and intuitive, enabling the collaborative exploration of efficient, expressive, and buildable compression-only forms [@Block2016; @Rippmann2013].

![COMPAS TNA framework overview.\label{fig:compas-tna}](../compas_tna.png)


<!-- # Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text. -->

<!-- # Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)" -->

<!-- # Figures

Figures can be included like this:
![COMPAS TNA framework overview.\label{fig:compas-tna}](../compas_tna.png)
and referenced from text using \autoref{fig:compas-tna}.

For a quick reference, the following figure commands can be used:
- `\autoref{fig:compas-tna}` -> "Figure 1"
- `\ref{fig:compas-tna}` -> "1"

Figure sizes can be customized by adding an optional second parameter:
![COMPAS TNA framework overview.](../compas_tna.png){ width=50% } -->

<!-- # Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project. -->

# References