# Battleship

The game, but more involved

## Offense

![alt text](./README_files/offense.PNG)

## Defense

Use a radar to help defend

```python
from radar import Radar

radar = Radar(range=[100, 150], theta=[30, 70], phi=[10, 20])

fig = radar.plot()
fig.show()
```

![alt text](./README_files/defense.PNG)
