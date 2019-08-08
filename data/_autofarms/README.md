## Format:

Autofarms require:
+ Build materials
+ Inputs/hr
+ Outputs/hr

As a result, the format is a json structured as follows:

```
{
    <str>: { # Name of autofarm
        "Build Cost": {
            <str>: <int>, # Item Name: Quantity
            ...
        },
        "Inputs": {
            <str>: <int>, # Item Name: Quantity
            ...
        },
        "Outputs": {
            <str>: <int>, # Item Name: Quantity
            ...
        },
        "Size": [<int>, <int>, <int>], # x,y,z
        "URL": <str>
        "Additional Comments": <str>
    },
    ...
}
```