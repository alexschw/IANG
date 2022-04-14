
from ANNarchy import Neuron, Synapse, Population, Projection, Uniform, Oja, compile
#   Bar Learning example
#
#   authors: Julien Vitay, Helge Uelo Dinkelbach

# Input neuron: r is set externally
InputNeuron = Neuron(parameters="r = 0.0")

# Leaky neuron
LeakyNeuron = Neuron(
    parameters="""
        tau = 10.0 : population
    """,
    equations="""
        tau * dr/dt + r = sum(exc) - sum(inh) : min=0.0
    """
)

# Creating the populations
Input = Population(geometry=(8, 8), neuron=InputNeuron, name='Input')
Feature = Population(geometry=(8, 4), neuron=LeakyNeuron, name='Feature')

# Creating the projections
ff = Projection(
    pre=Input,
    post=Feature,
    target='exc',
    synapse = Oja
)
ff.connect_all_to_all(weights = Uniform(-0.5, 0.5))
ff.min_w = -10.0

lat = Projection(
    pre=Feature,
    post=Feature,
    target='inh',
    synapse = Oja
)
lat.connect_all_to_all(weights = Uniform(0.0, 1.0))
lat.alpha = 0.3

compile()
