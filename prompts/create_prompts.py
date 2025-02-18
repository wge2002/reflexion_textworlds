import json

react_easy_0 = '''
You are hungry! Let's cook a delicious meal. Check the cookbook in the kitchen for the recipe. Once done, enjoy your meal!
-= Corridor =-
You arrive in a corridor. A normal one.
There is an exit to the north. There is an exit to the south. There is an exit to the west. Don't worry, there is no door.

> think: I can only perform 50 actions in this mission, so I want to complete as many effective actions as possible, such as finding food or handling food.  
OK.
> think: To solve the task, I need to use ingredients and the cookbook to cook a delicious meal and eat it.  
OK.
> think: First I need to go to the kitchen. There's three way to go, go west, go south, go north. I can check one by one, starting with go west.
OK.
> go west
-= Kitchen =-
You're now in a kitchen. Let's see what's in here.
You make out a closed conventional looking fridge nearby. You rest your hand against a wall, but you miss the wall and fall onto an oven. You make out a table. On the table you see a knife. You see a counter. I guess it's true what they say, if you're looking for a counter, go to TextWorld. The counter is vast. On the counter you can make out a cookbook. Look out! It's a- oh, never mind, it's just a stove. The stove is conventional. But oh no! there's nothing on this piece of junk.
There is a closed frosted-glass door leading west. There is an exit to the east. There is an exit to the north.
> think: Now I am in the kitchen, and I need to check the cookbook.
OK.
> examine cookbook
You open the copy of "Cooking: A Modern Approach (3rd Ed.)" and start reading:
Recipe #1
---------
Gather all following ingredients and follow the directions to prepare this tasty meal.
Ingredients:
yellow potato
Directions:
slice the yellow potato
  fry the yellow potato
  prepare meal
> think: To cook the meal, I need to find yellow potato. Food can only be find in inventory, kitchen or garden. I should first test myself, inventory, and search in kitchen and garden if not find. 
OK.
> inventory
You are carrying: a raw yellow potato, a yellow apple and a raw red potato.
> think: I only need yellow potato. So I need to drop yellow apple and red potato step by step.I can start with yellow apple.
OK.
> drop yellow apple
You drop the yellow apple on the ground.
> drop red potato
You drop the red potato on the ground.
> think: Now I have yellow potato, and I need to slice the yellow potato. I can use knife to slice the yellow potato. So I need to find the knife and slcie the yellow potato step by step.
OK.
> think: I remember there is a knife on the table, I should take it.
OK.
> take knife from table
You take the knife from the table.
> think: I have yellow potato and knife, I can slice the yellow potato.
OK.
> slice yellow potato with knife
You slice the yellow potato.

Your score has just gone up by one point.
> think: Next I need to fry the yellow potato. We have three tools to cook. The stove is to fry, oven to roast and BBQ to grill. So to fry, i choose stove. 
OK.
> think: I remember there is a stove in the kitchen. I can fry the yellow potato with stove.
OK.
> cook yellow potato with stove
You fried the yellow potato.

Your score has just gone up by one point.
> think: Now I can prepare meal and eat it.
OK.
>  prepare meal
Adding the meal to your inventory.

Your score has just gone up by one point.
> eat meal
You eat the meal. Not bad.

Your score has just gone up by one point.

                               *** The End ***
You scored 4 out of a possible 4, in 11 turns.

Would you like to RESTART, RESTORE a saved game, QUIT or UNDO the last command?
> 
'''

dict = {
    "react_easy_0" : react_easy_0
}

json_data = json.dumps(dict)

# 打印 JSON 字符串
print(json_data)

# 也可以将 JSON 数据保存到文件中
with open('/home/wge/git/reflexion/textworld_runs/prompts/tw_prompts.json', 'w') as f:
    json.dump(dict, f)