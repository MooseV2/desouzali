---
layout: post
comments: true
disqus: true
cover: 'assets/images/dna.jpg'
title: Optimization Using Genetic Algorithms
date:   2017-06-29 8:30:00
tags: genetic-algorithm machine-learning
navigation: True
logo: 'assets/images/ghost.png'
subclass: 'post'
categories: 'casper'
js:
- math
- fabric
- chart
---
Whether it's minimizing manufacturing costs, finding the [shortest path around a city](https://en.wikipedia.org/wiki/Travelling_salesman_problem), or finding an optimal airfoil design, optimization problems are everywhere. An **optimization problem**, simply put, is the problem of finding the *best* solution from all feasible solutions.

But how would you determine the best solution? *That* is the million dollar question. Suppose you were tasked with creating a box to hold liquid. The requirements state that the **area** must be at least **16m<sup>2</sup>** and every meter of material used in the **perimeter** costs **$2.00**. What's the cheapest box you can build?

<form id="formBoxOptim">  
  <fieldset>  
    <legend>Box optimization</legend>
    <em>Drag the box corners to resize</em>
    <canvas id="canvasBoxOptim" width="100%" height="250px"></canvas>
    <table>
      <tr>
        <td><label>Box Length</label></td>
        <td><input type="text" name="boxLength" disabled="true" size="6"></td>
      </tr>
      <tr>
        <td><label>Box Width</label></td>
        <td><input type="text" name="boxWidth" disabled="true" size="6"></td>
      </tr>
      <tr>
        <td><label>Area (\( L \times W \))</label></td>
        <td><input type="text" name="boxArea" disabled="true" size="6"></td>
      </tr>
      <tr>
        <td><label>Perimeter (\( 2L + 2W \))</label></td>
        <td><input type="text" name="boxPerimeter" disabled="true" size="6"></td>
      </tr>
      <tr>
        <td><label>Cost (\( \$2.00 \times Perimeter \))</label></td>
        <td><input type="text" name="boxCost" disabled="true" size="6"></td>
      </tr>
    </table>
  </fieldset>
  <script>
    function updateBox(e) {
      var box = e.target || e;
      var length = Math.round(box.getWidth() / 200 * 4)
      var width = Math.round(box.getHeight() / 200 * 4)
      var area = length * width;
      var perimeter = 2 * length + 2 * width;
      var cost = 2 * perimeter;
      var form = document.getElementById("formBoxOptim").elements;
      form["boxLength"].value = length;
      form["boxWidth"].value = width;
      form["boxArea"].value = area;
      form["boxPerimeter"].value = length;
      form["boxCost"].value = "$" + cost + ".00";

      form["boxArea"].style.backgroundColor = area < 16 ? "#f7cac5" : "#c1f4d7"
    }

    var canvas = new fabric.Canvas("canvasBoxOptim");
    canvas.setWidth(document.getElementById("formBoxOptim").offsetWidth);
    canvas.calcOffset();
    canvas.uniScaleTransform = true;
    var rect = new fabric.Rect({
      left: 20,
      top: 20,
      fill: 'red',
      width: 200,
      height: 100,
      transparentCorners: false
    });
    rect.setControlVisible("mtr", false);
    canvas.add(rect).setActiveObject(rect);
    canvas.on('object:scaling', updateBox);
    updateBox(rect);
  </script>
</form>
<br>

This problem is simple to solve mathematically. Working backwards from the required area of 16m<sup>2</sup>, we start by setting \\(16=L \cdot W \\) or \\(L = \frac{16}{W} \\) and substitute that into the equation for the perimeter:
\\[
  \begin{align}
    P &= 2W - 2\cdot(16\div W) \\\
      &= W - 16\div W \\\
      &= W^{2} - 16 \\\
    W &= 4 \\\
    L &= W = 4
  \end{align}
\\]

**Solution:** The cheapest box with an area of 16m<sup>2</sup> is 4 x 4m and costs $32.00.

Gradeschool level math is sufficient in solving equations with simple relationships and few variables, but what about more complex problems?

## Enter Genetics

It turns out that life on Earth is incredibly complex. *Trillions* of living cells interact every day to make up the body known as *you*. From a strictly biological point of view, life is a game where the objective is to stay on Earth as long as possible. The cells in your body can't keep this up forever, so the only possible way to prevent your own extinction is by duplicating the important parts of your own existence and making ... a *new* version of you. This, of course, is called *reproduction*.

Not every living creature makes the cut. Some are killed early -- by hunting, disease, or starvation. Some just can't find a suitable partner. If you're an African impala and constantly being hunted by carnivourous predators, there's no guarantee that you'll live long enough to ensure your spot in the gene pool.


<img src="{{ site.baseurl }}assets/images/impala.jpg" alt="An impala grazing in a field" style="width: 110%;">

But if you *did* have to outrun a lion, might your odds be *slightly* more favourable if you could run just a *little* bit faster, jump a *little* bit higher, and see a *little* bit farther? Over time, the less fortunate impalas would be killed off, leaving the faster impalas to reproduce and pass on their "code".

This "code" is found in every living organism in a special chemical called DNA, and among other things is responsible for tweaking the aforementioned variables. 

Unlike computer code, a scientist looking at DNA would see a string of millions (or billions) of "bases" in the form of **A**, **C**, **G**, and **T**, representing the fundamental base chemicals of DNA. The code is divided into discrete sections called **chromosomes**, with two chromosomes forming a double-helix pair. Each chromosome affects the organism differently. For example, in humans (who have 23 pairs of chromosomes), the 23rd pair determines gender. Let's look at what a chromosome may look like:

>  ... ACAAGATGCCATTGTCCCCCGGCCTCCTGCTGCTGCTGCTCTCCGGGGCCACGGCCACCGCTGCCCTGCCCCTGGAGGGTGGCCCCACCGGCCGAGACAGCGAGCATATGCAGGAAG ...

Despite looking nonsensical, scientists have discovered that certain functional groups of code at certain locations are responsible for the biological traits found in the organism. These groups are called **genes**.

> ... CC**<mark class="red">ATGCCTAA</mark>**GCCCC**<mark class="blue">ATGACATGA</mark>**AACG ...

The highlighted sequences above represent the genes responsible for trait *X* and trait *Y* in the organism. Let explore how changing these (hypothetical) codes would have an effect on our impala:

|Location | Gene | Effect |
| :---:     | ---  |   ---  |
|<mark class="red">Red</mark>|ATG**CC**TAA| Runs slower |
|<mark class="red">Red</mark>|ATG**CA**TAA| Runs faster |
|<mark class="blue">Blue</mark>|ATG**ACA**TGA| Jumps higher |
|<mark class="blue">Blue</mark>|ATG**GGG**TGA| Jumps lower |

The perfect impala would have *both* beneficial traits (running faster *and* jumping higher) and would be more likely to out-compete the impala who drew both short sticks, running slower and jumping lower.

I hope the concept of natural selection is becoming evident: despite the randomness of genetics, better traits are more likely to stay in the gene pool and worse traits are more likely to be killed off.

Here's where it gets interesting: we can simulate the process of natural selection in a computer model to optimize any solution.

## The Infinite Monkey Theorem

> A monkey hitting keys at random on a typewriter keyboard for an infinite amount of time will almost surely type the complete works of William Shakespeare.
>
> -- [Infinite Monkey Theorem - Wikipedia](https://en.wikipedia.org/wiki/Infinite_monkey_theorem)

How difficult would it be to type a given text completely randomly? Is that even possible?

Suppose there are 50 keys on a typewriter, and each of those keys have an equal 1/50 probability of being pressed. The probability of typing the word "Hello" is as follows:


$$
\underbrace{(1/50)}_{\text{H}}\times
\underbrace{(1/50)}_{\text{e}}\times
\underbrace{(1/50)}_{\text{l}}\times
\underbrace{(1/50)}_{\text{l}}\times
\underbrace{(1/50)}_{\text{o}} = \frac{1}{312,500,000}
$$

Yikes! That's a one in over 300 *million* chance to get a simple five letter word! And "Hello World"? Even typing eleven new letters every second since the **beginning of the universe** wouldn't guarantee success.

Let's try a different approach; one inspired by genetics.

## Implementing a Genetic Algorithm


> The brush must draw by itself. 
> -- [Alan Watts](https://en.wikipedia.org/wiki/Alan_Watts)

Let's recreate this quotation. To simulate natural selection, we're going to take the following steps:

1. Create an initial population
2. Calculate fitness
3. Select best individuals
4. Crossover or mutate the genes
5. Repeat until successful

<script type="text/javascript">
  function toggleCode(e) {
    var checkbox = e.target;
    codeblocks = document.querySelectorAll('.dragons');
        codeblocks.forEach(function(block) {
          var classes = block.classList;
          if (checkbox.checked) {
            classes.remove("hidden");
          } else {
            classes.add("hidden");
          }
    });
  }

</script>

<div class="panel panel-danger">
  <div class="panel-heading">
    <h3 class="panel-title">WARNING: Here be dragons!</h3>
  </div>
  <div class="panel-body">
    <em>In this post, we'll look at the code that creates this example. If you're not interested in that, flip the toggle below to hide it.</em>
    <br/>
    <br/>
    
    <div class="onoffswitch center">
      <input type="checkbox" name="displayCode" class="onoffswitch-checkbox" id="myonoffswitch" onclick="toggleCode(event);" checked>
      <label class="onoffswitch-label" for="myonoffswitch">
          <span class="onoffswitch-inner"></span>
          <span class="onoffswitch-switch"></span>
      </label>
  </div>
  </div>
</div>

### Creating the initial population

We'll start by creating a population of 500 random strings with a length of 29 characters each (the length of our desired quotation). These strings represent a single **chromosome** in each individual.

{% dragons %}
{% highlight python %}

from random import choice
def get_initial_population(word_length, pop_size):
  population = [] # The empty population
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " # Letter A-Z, plus space.
  for _ in range(population_size): # Generate words for the population
    word = "".join(choice(letters) for _ in range(word_length))
    population.append(word)
  return population
{% endhighlight %}
{% enddragons %}

| Generated Chromosomes |
| :----------:      |
|TRWLSSXFY KMUZLJMWGYVLDN UMCQ|
|WVLMMZXZJVA LTDOHFZKVWTOTIZGR|
|CUQTSYBCNUTBVAUGGDJGOXZSKAZTK|
|NSZHRBYRXUJGTFQQQFYVBXPWXSOAZ|
|QPRYUXLXRZSUIICWEBFK CGOR IBR|
|ENLTWBNJXEBUOLMCGLVVUTIWGGEPM|
|TNRIFHW KMTGZYTNFWPTWUKBARTGU|
|NJYRKYMLHJOSMUMET IYXHM WCOWA|
|KC IPQ TMEBQSMGUODVHJBPZWGLRK|
|ISDVVEQYSVUBURPJAEEOCUXTPOXXA|
| *490 more...*|

### Calculating Fitness

Those words don't look anything like the quotation we're trying to recreate. But exactly *how* dissimilar are they? We need a quantifiable metric that can tell us exactly how close our chromosome (that is, the string) is to the the quotation. This is called a [**fitness function**](https://en.wikipedia.org/wiki/Fitness_function).

Fitness functions can come in many forms, but the general idea is that they're given an *input* (that is, our string) and they *output* a number between 0 and 1 depending on how close our input is to the goal (with 1 being most optimal/perfect).

In this example, a fitness score can be determined by calculating how many characters are both the *correct letter* and in the *correct location*.

{% dragons %}
{% highlight python %}
def get_fitness(word):
  fitness = 0
  goal = "THE BRUSH MUST DRAW BY ITSELF" # Set goal
  for position, letter in enumerate(word):
    if letter == goal[position]:
      fitness += 1 # Add fitness if correct position/letter
  fitness = fitness / len(goal) # Determine percent correct
  return fitness
{% endhighlight %}
{% enddragons %}

<pre style="font-size: 16pt">
SPU<mark> </mark>FNXTFLIV<mark>S</mark><mark>T</mark>EQIDJH<mark>B</mark>L<mark> </mark>K<mark>T</mark>FUVU
THE<mark> </mark>BRUSH MU<mark>S</mark><mark>T</mark> DRAW <mark>B</mark>Y<mark> </mark>I<mark>T</mark>SELF

Fitness: 6/29 characters correct = 0.208
</pre>

The purpose of our genetic algorithm is to get the fitness score of a chromosome to 1.00. That is, *all* letters will be correct and in correct position.

### Selecting the best

Now that we have a list of each member of the population and their respective fitness, we want to decide which ones should be selected to create the next generation.

One method to do this is called fitness proportionate or [Roulette Wheel Selection](https://en.wikipedia.org/wiki/Fitness_proportionate_selection). Imagine all the chromosomes are placed on a roulette wheel, with the size of their pie being their fitness (that is, less fit chromosomes will have smaller slices).

<form>
    <div class="well">
    <legend>Roulette Wheel Selection</legend>
      <canvas id="canvasRoulette" height="200"></canvas>
    </div>
</form>
<script type="text/javascript">
pieData = {
    datasets: [{
        data: [0.1034, 0.0690, 0.0690, 0.0690, 0.0345, 0.0345],
        backgroundColor: ['#f1c40f', '#d38737', '#cd7b3f', '#c76f47', '#c1634f', '#bc5757']

    }],
    labels: ['QTASWKYET KHJTWJKJTMZYKWFBRTM', 'ZMAUBVTNXOCKTQTORQGCOSVYLXLBE', 'VXKVOMTRSB HU Z PUXRFPXIJSFPR', 'JMROSRQNNBEKVDTMKDYRHHLIFUOHK', 'QPRYUXLXRZSUIICWEBFK CGOR IBR', 'TNRIFHW KMTGZYTNFWPTWUKBARTGU'],
};
pieOptions = {
  legend: {
      display: false
    },
}

var myPieChart = new Chart("canvasRoulette",{
    type: 'pie',
    data: pieData,
    options: pieOptions,
});
</script>

The higher the fitness (yellow), the more likely the marble will select the chromosome. The lower the fitness (red), the less likely.

{% dragons %}
To do this mathematically, we must:

1. Sort the chromosomes in descending order by fitness
2. Determine the **Sum** of all fitnesses
3. Generate a random number between 0 and the **Sum**
4. Starting at the top of the list, cumulatively add the fitnesses until the sum is greater than our random number. The chromosome in this position is our selection.
5. Repeat steps 3-5 for as many parents as we want.

{% highlight python %}
from random import uniform
"""
Step 1. Sort
"""
def sort_population(population):
  # Create tuple with `(chromosome, fitness)`
  population_fitness = [(word, get_fitness(word)) for word in population]
  sorted_population = sorted(population_fitness, key=lambda x: x[1], reverse=True)
  return sorted_population
"""
Step 2. Sum
"""
def get_total_fitness(population):
  return sum((x[1] for x in population))
"""
Step 3-4. Select a chromosome from the roulette wheel.
"""
def get_chromosome(population, total_fitness):
  random_val = uniform(0, total_fitness)
  cumulative_sum = 0 # Start at 0
  for word, fitness in population:
    cumulative_sum += fitness
    if cumulative_sum > random_val:
      return word
"""
Step 5. Select two parents
"""
def get_parents(sorted_population, total_fitness):
  parents = [get_chromosome(sorted_population, total_fitness) for _ in range(2)]
  return parents
{% endhighlight %}
{% enddragons %}

Let's go ahead and select two parents using our roulette wheel selection.

<pre style="font-size: 16pt">
Parents:
   NJYRKYML<mark>H</mark>JOSMUMET IYXHM WCOWA
   ENLTWBNJXEB<mark>U</mark>OLMCGLVVUTIWGG<mark>E</mark>PM
</pre>

For convenience, I've highlighted the correct areas in the same fashion as the fitness step.

### Crossover and Mutation
Modifying the chromosomes to create a fitter individual is the quintessential element of genetic algorithms. This is done by one of two methods:

**Crossover**: Two parents chromosomes are split and recombined (either down the middle, at a random point, or at multiple points) to create a new chromosome.
<pre style="font-size: 16pt">
Crossover:
   <mark class="blue">NJYRKYML<mark>H</mark>JOSMU</mark>MET IYXHM WCOWA
 + ENLTWBNJXEB<mark>U</mark>OL<mark class="red">MCGLVVUTIWGG<mark>E</mark>PM</mark>
 --------------------------------
   <mark class="blue">NJYRKYML<mark>H</mark>JOSMU</mark><mark class="red">MCGLVVUTIWGG<mark>E</mark>PM</mark>
</pre>

**Mutation**: A (typically random) change is made to the chromosome. This can be randomly adjusting (adding or subtracting) a value, swapping or changing the order of values, or randomly changing values.

<pre style="font-size: 16pt">
Mutation:
   AABBCDEF --> <mark>BBCC</mark>CDEF (adjustment)
   AABBCDEF --> <mark>CD</mark>BB<mark>AA</mark>EF (swapping)
   AABBCDEF --> AABB<mark>MPRZ</mark> (random change)
</pre>


Typically a combination of crossover and mutation is used with a ratio dependent on the problem being solved (for example, crossover with 10% chance of mutation).


{% dragons %}
{% highlight python %}
def crossover_chromosome(A, B):
  crossover_point = randrange(len(A)) # Choose a random point 
  new_chromosome = A[:crossover_point] + B[crossover_point:]
  return new_chromosome

def mutate_chromosome(chromosome):
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " # Letter A-Z, plus space.
  num_mutations = randrange(0, 5)
  chromosome = list(chromosome) # Convert to a list for mutation
  for _ in range(num_mutations):
    position = randrange(0, len(chromosome))
    chromosome[position] = choice(letters) # Select a new random letter
  return "".join(chromosome) # Convert back to string
{% endhighlight %}
{% enddragons %}

### Putting it all together

We can create populations and evaluate their members on fitness. We can select the best ones and use them to create new chromosomes from crossover and/or mutation. We have all the pieces we need to implement this algorithm. The last step is to repeat these continuously until we achieve our goal.

1. Create an initial random population pool
2. Repeat the following steps until we've reached our max fitness goal:
    1. Sort the current population pool by fitness
    2. Create a new empty population pool and fill it by:
        1. Selecting two parents using roulette wheel selection on the old pool
        2. Crossover and/or mutate the parents to create a daughter
        3. Add the daughter to the new pool
        4. Repeat until the new pool is of desired size
    3. Delete the old pool and set the current pool to the new population

{% dragons %}
{% highlight python %}
population_size = 500 # Number of chromosomes in our population
word_length = 29 # Length of each chromosome
population = get_initial_population(word_length, population_size)

for generation in range(500):
  population = sort_population(population) # Sort by fitness
  print("Gen %s: %s [%03f]" % (generation, population[0][0], population[0][1]))
  if population[0][1] == 1.00: # Stop if we've reached our goal
    print("Finished after %s generations!" % (generation, ))
    break
  total_fitness = get_total_fitness(population)
  new_population = []
  for _ in range(population_size):
    parents = get_parents(population, total_fitness) # Roulette Wheel Selection
    daughter = crossover_chromosome(parents[0], parents[1]) # Crossover
    if uniform(0, 100) > 85: # 15% chance to mutate
      daughter = mutate_chromosome(daughter)
    new_population.append(daughter) # Add the daughter to the pool
  population = new_population # Replace the old pool with new population
{% endhighlight %}
{% enddragons %}

### Results

Below are the results of running the genetic algorithm using our implementation. It took less than a second to successfully converge on our goal, and did so after *only 88 generations*! Remember the brute-force method we discussed earlier? Even using every computer in the world to generate random strings for the remainder of the universe would likely not yield the results that we achieved.

<div class="well scroll-y" style="max-height: 700px">
{% md %}
*Results of the Genetic Algorithm*

|Generation|Best Chromosome|Fitness|
|----------|---------------|-------|
|0|TGP YMYWOKHKZJZRCKPHTZ AAEDLG|0.137931
|1|LDX GHKGHOLPLTHRCKPHTZ AAEDLG|0.172414
|2|KSEKOTHBCRXDSBGWRI XIYPISVESQ|0.206897
|3|OWEEARCXHYOCRUQDGLFABO MGSALZ|0.275862
|4|TWEEARCXHYOCRUQDGLFAOPOIXSQOY|0.241379
|5|TSEKOTHBCRXDSBGWRI XIYPISSLFE|0.241379
|6|T MZJRMMUCMDSDRJREWRNPNOBSEQG|0.275862
|7|OWE ABUECHAMQUKGRAA MZK VSMLF|0.310345
|8|T EEAPASI XDSBGNRI XIYXIJSFAF|0.344828
|9|TXEEARCXHCXFHKRDRDN BYXIJSFAR|0.379310
|10|TWEEPRVBHYOCRAUDRI OZYPISSALF|0.379310
|11|I MZURUSHOMJD CYBAU JWAIPSELF|0.413793
|12|TXEEARCSI LRIA DREWOZYPISSALF|0.482759
|13|TWEHBBUSHCMJDPNFRQXGUYPISSALF|0.448276
|14|TWEHBBUSHOODSBUDRDNQNQOIPSELF|0.482759
|15|TWEHBBUSHOODSBUDRDNQNY AGSEXS|0.448276
|16|T EEAPOSHJUFSTUDRI  RYAIPSELF|0.517241
|17|OWECBJUSQ BKSTPDWPE RYAIPSELF|0.517241
|18|TWEEPRVBS XDSP DREWQPYJIPSELF|0.517241
|19|TXEEARCSI MBSTUDRI  RYAIPSELF|0.586207
|20|TWEHBBUSHOMCRUQDRDN BYXIJSLLF|0.551724
|21|TXEMBBUSHOMCRUQDRDN BYXIJSLLF|0.551724
|22|TXEMBBUSHOMCRUQDRDN BYXIJSLLF|0.551724
|23|T LHBBUSHJEUS FDREW BC IPSELF|0.620690
|24|TWEZBBUSHOMCRUQDRDN BYXIJSLLF|0.551724
|25|TWEHBBUSHCPCSBQDRDN BYXIJSLLF|0.551724
|26|LOE ARUSHOOKSTPDJMU JYPIPSELF|0.551724
|27|TEGHBBUSHXDUSAUDRDN BYVIPSELF|0.586207
|28|THMJBBUSHCMUSSPDRIFFJG IYSELF|0.586207
|29|TXEMBBUSHOMLNLEDREN BY IPSFLF|0.586207
|30|THEEBRUSHPADNBODRAEQBYDIDLELF|0.586207
|31|TSEGBBUSHCMUSMODRJUOBYDISSELF|0.620690
|32|THEEBRUSHPADNBODRAEQBY IZCELF|0.620690
|33|TWEHBVUSHCMJZTUDRIU JY IZSELF|0.620690
|34|T EHBBUSH XCSTPDREE BYXIESELF|0.655172
|35|THEEBRUSHOKUSTFDRIEOBY ISSXLF|0.689655
|36|THEEBRUSHOKUS WDREEQBY ISSXLF|0.655172
|37|TWEHKRUSH MFST DREWBTYWIXZELF|0.655172
|38|TXECBNUSCCMUSTQDRBN BY ISSELF|0.689655
|39|TSEGBRCSHCMDST DREWBSY IPSELF|0.689655
|40|TSEGBRUSCCMUSTQDRBN BY IVSELF|0.724138
|41|THEGBRUSCCMUSTQDRBN BY IVSELF|0.758621
|42|TWEEBRUSH MFST DREWBZY IZSESF|0.724138
|43|TWE GRUSHPMUSM DREW JYEIESELF|0.724138
|44|TWEEBRUSH MFST DTDEQBY IESELF|0.724138
|45|OHE KRUSH MFST DREWBZO IPSELF|0.724138
|46|TWEEBRUSH MFST DREWBZ  IFSELF|0.724138
|47|THZ BRUSH MUBTIDREW QY IPSELF|0.793103
|48|THZ KRUSHCMFST DRBN BY IVSELF|0.758621
|49|THLHBBUSH MFST DREN BY IVSELF|0.758621
|50|NHE QRUSHPMUST DREE QY IZSELF|0.758621
|51|THEEBRUSHCMFST DRAWRVY ISSGLF|0.758621
|52|THEEBBUSHCMFST DRAWRVY IPSELF|0.758621
|53|NHE ARUSHPMUST DRAN NO IPSELF|0.758621
|54|NHE ARUSHPMUST DRAWRVY IPSELF|0.793103
|55|NHE ARUSHPMUST DRAWRVY ISSELF|0.793103
|56|THE ARUSHPMUST DRAWRVY ISSELF|0.827586
|57|THEEBBUSHCMUST DRAWRVY ISSELF|0.793103
|58|OHE KRUSH MFST DREWQBY IOSELF|0.793103
|59|THEEURUSHCMUST DRAWRVY ISSELF|0.793103
|60|T EHBBUSH MPST DRAWEBY ISSELF|0.793103
|61|THEBBBUSH MPST DRAWEBY ISSELF|0.827586
|62|OHZ BRUSH MNST DRAWEBY ISSELF|0.827586
|63|THEBBRUSH MNST DRAWEBY ISSELF|0.862069
|64|THEEBBUSH MUSM DRAW BY IRSHLF|0.827586
|65|THE DRUSHPMUST DRAW BY IYSELF|0.896552
|66|THE BRUSHSMUST DRDW BW ISSELF|0.862069
|67|THE BRUSHXMUST DRAJ RY IOLELF|0.827586
|68|OHE BRUSH MUSM DRAC DY ISSELF|0.827586
|69|THZTBRUSH MUST DRAW BY IBSBLF|0.862069
|70|THEEBBUSH MUST DRAJ BYDIXSELF|0.827586
|71|THE BRUSH MUST DRAU BZNIJSELF|0.862069
|72|THE BRGDH MUST DRAJ BY IPSELZ|0.827586
|73|THE BRUSHMQUST DRAW BY ISSELF|0.896552
|74|THE BRUSH MUST DRAJ BW ISSELF|0.896552
|75|THE BRBSH MHST DRAW BY IBSELF|0.896552
|76|THE BRBSH MHST DRAW BY ISSELF|0.896552
|77|THE KRUSH MUST DRAJ BY ISSELF|0.896552
|78|THEEBRUSH MUST DRAW BY IBSELF|0.931034
|79|THE BRUSH MUST DRAJ DY ISSELF|0.896552
|80|THEEBRUSH MUST DRAW BY IXSELF|0.931034
|81|THE DRUSH MUST DRDW BY ISSELF|0.896552
|82|THEEBRUSH MUST DRAW BY ILSETF|0.896552
|83|THEBBRUSH MUST DRAW BY IUSERF|0.896552
|84|THEEMRUSH MUST DRAW BY IUSELF|0.896552
|85|THE BRUSH MUSTPDRAW BY IBSELF|0.931034
|86|THE BRUSH MUSTPDRAW BY IBSELF|0.931034
|87|THE BRUSH MUST DRAW BY IUSELF|0.965517
|88|THE BRUSH MUST DRAW BY ITSELF|1.000000
{% endmd %}
</div>

One last time, let's go over the benefits of genetic algorithms:

1. They're inspired by the ingenuity of nature: the same process that created all of life.
2. They're (relatively) easy to implement in little code.
3. They can easily be applied to a wide variety of problems.
4. They're *significantly* more efficient than a brute-force approach.

There are many more aspects to genetic algorithms that haven't been covered. Future posts will introduce things such as elitism, encoding, and different selection methods.

Lastly, I leave you with a tool to play with the implementation we devised. Play around with the parameters: see how long a lengthly goal takes to succeed, or how a small population or low mutation rate will affect the evolution process. All the code (both the Python and JavaScript versions) are available through the links at the bottom of the page.

### Play with it

<form id="formGenAlg">  
  <fieldset>  
    <legend>Genetic Algorithm</legend>
    <table>
      <tr>
        <td><label>Goal</label></td>
        <td><input type="text" name="gaGoal" size="40" value="HELLO WORLD"></td>
      </tr>
      <tr>
        <td><label>Population Size</label></td>
        <td><input type="text" name="gaPopSize" size="6" value="1000"></td>
      </tr>
      <tr>
        <td><label>Mutation Rate</label></td>
        <td><input type="text" name="gaMutationRate" size="3" value="15"><label> %</label></td>
      </tr>
      <tr>
        <td></td>
        <td><input type="button" onclick="runSim();" value="Run Genetic Algorithm"></input></td>
      </tr>
      </table>
      <div id="gaResultsScroll" class="well scroll-y" style="max-height: 500px">
        <table>
          <thead>
            <tr>
              <td><strong>Generation</strong></td>
              <td><strong>Chromosome</strong></td>
              <td><strong>Fitness</strong></td>
            </tr>
          </thead>
          <tbody id="gaResults">
          </tbody>
        </table>
      </div>
  </fieldset>
</form>

<script type="text/javascript">
  table = document.getElementById("gaResults");
  // Add cells to results table from array
  function addToTable(cells) {
    var fragment = document.createDocumentFragment();
    var row = document.createElement("tr");

    for (var i = 0; i < cells.length; i++) {
      var cell = document.createElement("td");
      cell.appendChild(document.createTextNode(cells[i]));
      row.appendChild(cell);
    }
    fragment.appendChild(row);
    table.appendChild(fragment);
  }

  // Clears entire results table
  function clearTable() {
    while (table.firstChild) {
      table.removeChild(table.firstChild);
    }
  }


  // Code style to reflect Python in example

  // Create initial population
  function get_initial_population(word_length, pop_size, goal) {
    var chromosome, letters;
    var population = [];
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "; //A-Z and space
    for (var i = 0; i < pop_size; i++) {
      chromosome = "";
      for(var j = 0; j < word_length; j++) {
          chromosome += letters.charAt(Math.floor(Math.random() * letters.length));
      }
      population.push([chromosome, get_fitness(chromosome, goal)]);
    }
    return population;
  }

  function get_fitness(chromosome, goal) {
    var fitness = 0;
    for (var i = 0; i < chromosome.length; i++) {
      if (chromosome[i] === goal[i]) {
        fitness++;
      }
    }
    fitness = fitness / chromosome.length;
    return fitness;
  }

  function sort_population(population) {
    return population.sort(function(a,b) { return b[1] - a[1]; });
  }

  function get_total_fitness(population) {
    return population.map(function(v) { return v[1]; })
                     .reduce(function(a,b) { return a + b; });
  }

  function get_chromosome(population, total_fitness) {
    var random_val = Math.random() * total_fitness;
    var cumulative_sum = 0;
    for (var i = 0; i < population.length; i++) {
      cumulative_sum += population[i][1];
      if (cumulative_sum > random_val)
        return population[i][0];
    }
  }

  function get_parents(population, total_fitness) {
    var parents = [];
    for (var i = 0; i < 2; i++) {
      parents.push(get_chromosome(population, total_fitness));
    }
    return parents;
  }

  function crossover_chromosome(A, B) {
    var crossover_point = Math.floor(Math.random() * (A.length));
    return A.slice(0, crossover_point + 1) + B.slice(crossover_point + 1, B.length);
  }

  function mutate_chromosome(chromosome) {
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "; //A-Z and space
    var num_mutations = Math.floor(Math.random() * 5);
    while (num_mutations--) {
      var position = Math.floor(Math.random() * chromosome.length);
      chromosome[position] = letters.charAt(Math.floor(Math.random() * letters.length));
    }
    return chromosome;
  }

  function spawnMonkeys(pop_size, goal, mutate_rate) {
    goal = goal.toUpperCase();
    var word_length = goal.length;
    var population = get_initial_population(word_length, pop_size, goal);

    for (var generation = 0; generation < 1000; generation++) {
      population = sort_population(population);
      addToTable([generation, population[0][0], population[0][1].toFixed(4)]);
      if (population[0][1] === 1.00) {
        table.appendChild(document.createTextNode("Finished after " + generation.toString() + " generations."));
        break;
      }
      var total_fitness = get_total_fitness(population);
      var new_population = [];
      for (i = 0; i < pop_size; i++) {
        var parents = get_parents(population, total_fitness);
        var daughter = crossover_chromosome(parents[0], parents[1]);
        if (Math.random() * 100 > (100 - mutate_rate)) {
          daughter = mutate_chromosome(daughter);
        }
        new_population.push([daughter, get_fitness(daughter, goal)]);
      }
      population = new_population;
    }
  }

  function runSim() {
    clearTable();
    form = document.getElementById("formGenAlg").elements;
    var goal = form["gaGoal"].value;
    var pop_size = form["gaPopSize"].value;
    var mutate_rate = Math.min(100, Math.max(0, form["gaMutationRate"].value));
    spawnMonkeys(pop_size, goal, mutate_rate);
    var scrollDiv = document.getElementById("gaResultsScroll");
    scrollDiv.scrollTop = scrollDiv.scrollHeight;
  }
</script>

### Source code

Available in the near future. Check back soon!