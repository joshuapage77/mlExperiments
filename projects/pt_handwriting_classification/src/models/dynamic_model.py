import torch.nn as nn
import torch.nn.functional as F
import torch

import torch
import torch.nn as nn

class DynamicModel(nn.Module):
   def __init__(
      self,
      num_classes=26,
      num_hidden_layers=2,
      channels=[32, 64],
      downsample=['pool', 'strided'],
      activation='relu',
      fc_activation='relu',
      fc_units=[128],
      use_fc_dropout=False,
      input_shape=(1, 28, 28)
   ):
      super().__init__()

      channels = self._fit_to_layer_depth(channels, num_hidden_layers)
      downsample = self._fit_to_layer_depth(downsample, num_hidden_layers)

      if isinstance(activation, str):
         activation = [activation]
      self.activations = self._fit_to_layer_depth(activation, num_hidden_layers)

      self.fc_activation = self._get_activation(fc_activation)
      self.use_fc_dropout = use_fc_dropout
      self.dropout = nn.Dropout(0.5) if use_fc_dropout else nn.Identity()

      self.conv_blocks = nn.ModuleList()
      in_channels = input_shape[0]

      for i in range(num_hidden_layers):
         out_channels = channels[i]
         block = []

         # Convolution
         block.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1))

         # Downsampling
         ds = downsample[i]
         if ds == 'pool':
            block.append(nn.MaxPool2d(2, 2))
         elif ds == 'strided':
            block.append(nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=2, padding=1))

         self.conv_blocks.append(nn.Sequential(*block))
         in_channels = out_channels

      # Compute flattened feature size (on model's device)
      dummy_input = torch.zeros((1, *input_shape), device=next(self.parameters()).device)
      with torch.no_grad():
         for i, block in enumerate(self.conv_blocks):
            dummy_input = block(dummy_input)
            dummy_input = self._get_activation(self.activations[i])(dummy_input)
      flat_features = dummy_input.view(1, -1).size(1)

      # Fully connected layers
      self.fcs = nn.ModuleList()
      fc_sizes = [flat_features] + fc_units + [num_classes]
      for i in range(len(fc_sizes) - 1):
         self.fcs.append(nn.Linear(fc_sizes[i], fc_sizes[i + 1]))

   def _get_activation(self, name):
      return {
         'relu': nn.ReLU(),
         'leaky_relu': nn.LeakyReLU(),
         'elu': nn.ELU(),
         'tanh': nn.Tanh()
      }.get(name.lower(), nn.ReLU())

   def _fit_to_layer_depth(self, lst, target_len):
      if len(lst) == target_len:
         return lst
      elif len(lst) == 1:
         return [lst[0]] * target_len
      elif len(lst) < target_len:
         first = lst[0]
         last = lst[-1]
         middle = lst[1] if len(lst) > 1 else last
         fill = [middle] * (target_len - 2)
         return [first] + fill + [last]
      else:
         return [lst[0]] + [lst[-1]] if target_len == 2 else [lst[0]] + lst[1:target_len - 1] + [lst[-1]]

   def forward(self, x):
      for i, block in enumerate(self.conv_blocks):
         x = block(x)
         x = self._get_activation(self.activations[i])(x)

      x = x.view(x.size(0), -1)

      for i, layer in enumerate(self.fcs):
         x = layer(x)
         if i < len(self.fcs) - 1:
            x = self.fc_activation(x)
            x = self.dropout(x)

      return x
