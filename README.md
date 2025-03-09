# Wheat Delivery Optimization Problem

So I came across this problem from my friend: 

> You need to deliver 300kg of wheat to a factory and the factory is located 100km away from your place.
> 
> You have a carriage which able to carry maximum 100kg of wheat each time, but the horse needs to eat/consume 1kg of wheat for every 1km it travels.
> 
> Any way would you do to deliver the most wheat to the factory?

I only managed to get a sub-optimal solution by hand calculations and I am not sure how to convert it into a script. 

Thanks to the idea from the internet and GPT, I finally made a script to find the optimal number of stops and where to stop to deliver the most wheat (only to feed my curiosity).

These equations helped me in writing the script:

<code> 300 - 5x = 200 </code> (200kg to be delivered with 3 forward and 2 backward trips, so x will be a checkpoint/stop at 20km)

<code> 200 - 3y = 100 </code> (100kg to be delivered with 2 forward and 1 backward trip, so y will be a stop at 53km)

But I am too dumb to understand why we use 200 and 300 here, so I decided to write a script to run through all possible stops, as well as all possible numbers of stops (not only x and y) 🫤.
