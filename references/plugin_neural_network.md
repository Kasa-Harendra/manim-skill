# manim-neural-network Plugin Reference Guide

`manim-neural-network` provides customizable mobjects for visualizing fully connected feed-forward artificial neural networks, including layer-to-layer connections, mathematical neuron labeling, and forward pass signals.

- **Repository**: [https://github.com/JPM2002/manim-neural-network](https://github.com/JPM2002/manim-neural-network)
- **Author**: JPM2002
- **Package**: `manim-neural-network`
- **Import Namespace**: `manim_neural_network.neural_network`

---

## 1. Installation & Setup

```bash
pip install manim-neural-network
```

Import in your script:
```python
from manim import *
from manim_neural_network.neural_network import NeuralNetworkMobject
```

---

## 2. Core API: `NeuralNetworkMobject`

Constructs a multi-layer perceptron by passing a list of layer sizes:

```python
nn = NeuralNetworkMobject([3, 5, 4, 2])
```

### Key Attributes for Customization
| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `neuron_radius` | `float` | `0.15` | Radius of each neuron circle |
| `neuron_to_neuron_buff` | `float` | `0.2` | Vertical spacing between neurons in a layer |
| `layer_to_layer_buff` | `float` | `1.0` | Horizontal spacing between adjacent layers |
| `input_neuron_color` | `Color` | `WHITE` | Stroke color for input layer neurons |
| `hidden_layer_neuron_color` | `Color` | `WHITE` | Stroke color for hidden layer neurons |
| `output_neuron_color` | `Color` | `WHITE` | Stroke color for output layer neurons |
| `edge_color` | `Color` | `LIGHT_GREY` | Line color for synaptic connections |
| `edge_stroke_width` | `float` | `2.0` | Line thickness for synaptic weights |
| `neuron_fill_opacity` | `float` | `1.0` | Fill opacity of neuron interiors (`fill_color=BLACK`) |

### Labeling Methods
- `nn.label_inputs(label="x")`: Generates $x_1, x_2, \dots$ to the left of the input layer.
- `nn.label_outputs(label=r"\hat{y}")`: Generates $\hat{y}_1, \hat{y}_2, \dots$ to the right of the output layer.
- `nn.label_layers(labels=["Input", "Hidden 1", "Output"])`: Places descriptive labels directly above each layer column.

---

## 3. Production Recipe: Forward Activation Flow

```python
from manim import *
from manim_neural_network.neural_network import NeuralNetworkMobject

class NeuralNetworkScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Deep Neural Network: Feed-Forward Propagation}", font_size=32).to_edge(UP, buff=0.5)
        self.add(title)

        # 1. Instantiate 4-layer network: 3 inputs -> 5 hidden -> 4 hidden -> 2 outputs
        nn = NeuralNetworkMobject([3, 5, 4, 2])
        nn.input_neuron_color = BLUE_C
        nn.hidden_layer_neuron_color = TEAL_C
        nn.output_neuron_color = YELLOW_C
        nn.edge_color = GRAY_D
        nn.edge_stroke_width = 1.2
        nn.shift(DOWN * 0.3)

        # 2. Add annotations
        nn.label_inputs("x")
        nn.label_outputs(r"\hat{y}")
        nn.label_layers(["Input", "Dense 1", "Dense 2", "Output"], input_size=0.3, hidden_size=0.25, output_size=0.3)

        # 3. Animate creation
        self.play(Create(nn), run_time=2.0)
        self.wait(0.5)

        # 4. Animated forward propagation wave (3b1b dynamic pulse)
        for i, layer in enumerate(nn.layers):
            self.play(
                layer.neurons.animate.set_fill(YELLOW_C, opacity=0.8),
                run_time=0.4
            )
            if i < len(nn.layers) - 1:
                self.play(
                    nn.edge_groups[i].animate.set_stroke(color=YELLOW_A, width=2.5),
                    run_time=0.3
                )
                self.play(
                    nn.edge_groups[i].animate.set_stroke(color=GRAY_D, width=1.2),
                    layer.neurons.animate.set_fill(BLACK, opacity=1.0),
                    run_time=0.3
                )

        # Final output highlight
        self.play(Circumscribe(nn.layers[-1], color=YELLOW_C, fade_out=True))
        self.wait(1)
```

---

## 4. Best Practices

1. **Layer Sizing**: Keep neuron counts per layer below 8–10 in explainer videos to prevent visual clutter; use vertical ellipses ($\dots$) if representing wide dimensions.
2. **Visual Hierarchy**: Keep synaptic connections subtle (`stroke_width=1.0 - 1.5`, `color=DARK_GREY` or `GRAY_D`) so active pulses and neuron activations stand out vividly.
