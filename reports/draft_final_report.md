# Self-Organized Critical Properties of Earthquakes through Cellular Automata-based Models
### Evan New-Schmidt, Matt Brucker

### Abstract

In the physical world, earthquakes have been found to follow a law known as the Gutenberg-Richter law[[2]](http://downloads.gphysics.net/papers/BakTang_1989.pdf): the number of earthquakes that occur follows a power-law distribution relative to the size of the earthquake. One potential explanation for this, initially proposed by Bak and Chen, is that the crust of the earth is in a self-organized critical state. They explore this possibility by modeling the earth's crust as a grid of sliding blocks, with each block sitting on a stationary plate and attached to a sliding plate as well as its neighbors with springs. Each block has a certain static friction force which, when overcome by the forces due to the springs, causes the block to slip and redistribute forces to its neighbors. In this paper, we replicate a similar model proposed by Olami, Feder, and Christensen[[1]](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.68.1244), which differs from Bak and Chen's model in that it's nonconservative; blocks have an elasticity coefficient that controls how much force is transfered when slipping occurs, and thus energy is lost from the system. We simulate this model and find that the system follows a power-law distribution over a range of values of elasticity coefficients, making it likely that it's a self-organized critical system. We further explore the other features of self-organized critical systems, pink noise and fractal geometry, to determine the robustness of the system's self-organized critical properties. We find that energy conservation isn't a requirement for self-organized criticality, as the system displays a number of self-organized critical traits across a range of elasticity coefficients.

### Power-Law Behavior of Earthquakes
Based on empirical data, Gutenberg and Richter[[2]](http://downloads.gphysics.net/papers/BakTang_1989.pdf) found that the number of earthquakes N above a certain size m that occur follows the distribution:

>>> Insert image of distribution

where *a* and *b* are constants that vary depending on the location of the earthquake. The exact cause of this phenomenon is unknown, but a possible explanation is that this occurs because of the geometry of fault lines; fault lines have been found to exhibit fracticality, which along with the power-law feature hints toward the potential that earthquakes exist in a self-organized critical state. Thus we can use a simplified model to help explain how this phenomenon occurs.

### A Cellular Automaton-based Model for Earthquakes

Olami, Feder, and Christensen[[1]](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.68.1244) propose a model for earthquakes based on cellular automata. The earthquake is represented as a grid of sliding blocks; each block sits on a stationary plate and is attached to a moving plate, as well as its neighbors, by springs. This system is represented by an NxN grid of cellular automata, where each cell represents a single block. The forces on each block are determined by the position of the block, the position of its neighbors, and the spring constants between everything:

>>> Insert equation for forces

where *K1* is the spring constant of horizontal neighbors, *K2* is the spring constant of vertical neighbors, and *KL* is the spring constant connecting to the sliding plate.  

There are **ADD THIS** phases to the earthquake model:
1. *Initialization:* Each block is initialized


### Bibliography

[1] [Self-Organized Criticality in a Continuous, Nonconservative Cellular Automaton Modeling Earthquakes](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.68.1244)  
*Olami, Zeev; Hans Jacob S. Feder; and Kim Christensen.* Physical Review Letters, Vol. 68 Number 8.

Olami, Feder, and Christensen explore the applications of modeling earthquakes' occurrence through cellular automata, building on previous work that shows the power-law distribution of earthquakes. They model earthquakes through a sliding-block model consisting of two plates, one fixed and one moving, with a two-dimensional grid of blocks between them. The blocks are attached by springs to the moving plates, held by friction to the fixed plate, and attached to their neighboring blocks by springs. Each block has a maximum friction force, after which the block starts moving, reaching an equilibrium state and redistributing its force to its neighbors. They simulate this system, analyzing the probability of earthquakes occurring with a given energy, and examining the effect of varying the elasticity (i.e. how much force is distributed to other blocks when one block slides). They find that the system exhibits a power law distribution over a long range of energy conservation values, and even with the introduction of noise; they also find that the exponent of the power law distribution is dependent on the value of the elasticity parameter. They also find that the system has a state of metastability, where it's stable until it crosses a certain threshold. They believe this to be a fundamental property of modeling earthquakes.

[2] [Earthquakes as a Self-Organized Critical Phenomenon](http://downloads.gphysics.net/papers/BakTang_1989.pdf)  
*Bak, Per, and Chao Tang.* Journal of Geophysical Research, Vol. 94 Number B11. Published November 10, 1989.

In this paper, Bak and Tang propose a model to explain the distribution of earthquake energies as determined by empirical data. To answer this question, they build off of existing models that represent faults as a network of blocks connected by springs and connected to two plates, one fixed and one sliding. They represent this model through a cellular automata simulation, with each cell representing a single block. Random stresses are added to individual blocks each timestep; once a block reaches a critical level of stress, it slips and distributes its stress to its neighbors. After a certain amount of total stress has been added to the system, it reaches a critical state in which stresses may trigger any size of earthquake, only bounded by the size of the model. From this model, they find that the magnitudes of earthquakes follow a power-law distribution in this state. Their model builds on previous models of earthquakes, but it adds the critical step of observing the power-law distribution of earthquake magnitudes. They conclude that their model may be an explanation of how this power-law distribution came to be in earthquakes in the natural world.

[3] [Unified Scaling Law for Earthquakes](https://arxiv.org/pdf/cond-mat/0112342.pdf)
P Bak, K Christensen, L Danon, T Scanlon - Physical Review Letters, 2002 - APS

Bak et al. look at earthquake data in California, specifically waiting times and estimate their fractal dimension. They find that there is no meaningful difference between aftershocks and main shocks, and a power-law correlation between waiting times and magnitude. Plotting recorded earthquake epicenters on a 2-dimensional map, they find that grouping earthquakes by magnitude yields a fractal dimension of 1.2. They frame earthquakes as processes that produce sequences of correlated earthquakes, similar to SOC avalanche models. This framing is similar to the models proposed in Zeev et al. and Bal et al., and offers potential methods of observing fractal dimension in those models to compare with actual earthquake data.
