# Bug/Ant Life Simulation
Date: 1/2024

## Reasons for why / Technologies used

The only reason why I made this project was because I was walking on the sidewalk and looked down then I saw an Ant walking and instantly I though "I want to make something like you".
So I decided the best way to approach this was to use pygame to create the visuals and use the Vector classes, numpy to utilize optimized math calculations for a Neural Network, and multi-threading to speed up and optimize the flow of the program.


## Optimizations

In general, the system demonstrated functionality; however, there were several optimizations that I aimed to implement. Firstly, an improvement was necessary in the calculations of collisions and object detection. In the first iteration of the project the 'Bug' would each individually go through every other bug/fruit which caused my project to have a bottleneck based on the population size. Therefore, the first improvement was the implementation of Spatial Partitioning. This improved the project speed by going from O(n^2) for every object detection to O(n). 


## Run Locally

Clone the project

```bash
git clone https://github.com/Nocivofrank/BugLife.git
cd BugLife-main
```

Install dependencies:

```
pip install -r requirements.txt
```

Open terminal in project root directory and run

```bash
python main.py
```

## Authors

- [@Nocivofrank](https://www.github.com/Nocivofrank)

