#!/usr/bin/env python

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import (Base, Users, Cuisine, Recipe)

engine = create_engine('sqlite:///rb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

anony_user = Users(name="Anonymous", email='anonymous@gmail.com')
session.add(anony_user)
session.commit()

cuisines = [('Indian Cuisine', 1), ('American Cuisine', 2),
            ('Chinese Cuisine', 3), ('Italian Cuisine', 4)]
for cuisine in cuisines:
    entry = Cuisine(name=cuisine[0], id=cuisine[1])
    session.add(entry)
    session.commit()

this_user = session.query(Users).filter_by(name="Anonymous").one()


recipe = Recipe(
    name="Chicken Tikka Masala",
    ingredients="""
    7 garlic cloves, finely grated 4 tsp
    finely grated peeled ginger 4 tsp
    ground turmeric 2 tsp
    garam masala 2 tsp
    ground coriander 2 tsp
    ground cumin 1-1/2 cups whole-milk yogurt (not Greek) 1 Tbsp
    kosher salt 2 lb
    skinless, boneless chicken breasts, halved lengthwise 3 Tbsp
    ghee (clarified butter) or vegetable oil 1 small onion, thinly
    sliced 1/4 cup tomato paste 6 cardamom pods, crushed 2 dried chiles,
    1/2 tsp crushed red pepper flakes
    can whole peeled tomatoes, 2 cups heavy cream 3/4 cup chopped cilantro,
    plus sprigs for garnish Steamed basmati rice (for serving)
""",
    body="""Combine garlic, ginger, turmeric, garam masala, coriander,
    and cumin in a small bowl. Whisk yogurt, salt,
    and half of spice mixture in a medium bowl; add chicken and turn to coat.
    Cover and chill 4-6 hours. Cover and chill remaining spice mixture.
    Heat ghee in a large heavy pot over medium heat. Add onion, tomato paste,
    cardamom, and chiles and cook, stirring often, until tomato paste has
    darkened and onion is soft, about 5 minutes. Add remaining half of spice
    mixture and cook, stirring often, until bottom of pot begins to brown,
    about 4 minutes.
""",
    user_id=this_user.id,
    cuisine_id=1,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()


recipe = Recipe(
    name="Gulab Jamun",
    ingredients="""FOR SUGAR SYRUP:
    1 cup sugar
    1 cup water
    3 cardamom, powdered
    1 tbsp lemon juice
    FOR GULAB JAMUN:
    9 tbsp milk powder
    3-1/2 tbsp maida / all-purpose flour / plain flour
    1 tbsp rava / semolina / sooji
    pinch of baking soda
    1 tsp lemon juice
    1 tsp ghee / clarified butter
    4-5 tbsp milk, warm
""",
    body="""Serving Size-8,SUGAR SYRUP RECIPE:
    firstly, in a wide pan take 1 cup of sugar.
    further, to that add 1 cup of water and get to a boil.
    then simmer for 4 minutes till the sugar syrup turns slightly sticky.
    now add cardamom powder.
    also add lemon juice to stop crystallization process.
    cover and keep aside.
    GULAB JAMUN RECIPE:
    firstly in a large mixing bowl take milk powder.
    further, to that add maida and rava.
    then add pinch of baking soda
    also add ghee, lemon juice and crumble well.
    slowly add milk little by little and knead well.
    knead to a smooth and soft dough.
    furthermore, make small balls greasing ghee to hands.
    make sure there are no cracks on balls. else there are chances for gulab
    jamun to break while frying. Heat the ghee on low flame and when the ghee
    is moderately hot, fry the jamuns.
    fry the balls on low flame stirring in between.
    fry till the balls turns golden brown.
    immediately, drop the hot jamuns into hot sugar syrup.
    cover the lid and rest for 2 hours. flame should be turned off.
    finally, the jamuns have doubled in size.
""",
    user_id=this_user.id,
    cuisine_id=1,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()

recipe = Recipe(
    name="Cheese Burger",
    ingredients="""2 pounds	freshly ground chuck,
    1 tablespoon onion powder
    1 teaspoon salt
    1 teaspoon freshly ground black pepper
    12 slices deli-counter American cheese
    6 large burger buns, preferably homemade, toasted if desired,
    ketchup
    mayonnaise
    thousand island dressing
    sliced red onion
    sliced tomatoes
    sliced pickles
    fresh lettuce leaves

""",
    body="""Serving Size-6,In a large bowl, mix ground beef, onion powder,
    salt and pepper until just combined. Do not overmix, or your patties will
    be tough. Divide into six portions and form patties, without pressing too
    hard. They should be uniform in thickness. Smooth out any cracks using your
    fingers. Make these right before you grill them, so they stay at room
    temperature. Preheat your grill, grill pan or cast-iron skillet to high
    heat and add burger patties. If using a grill, cover with the lid.
    Cook until the crust that forms on the bottom of the burger releases
    it from the pan or grate about 2 minutes. Gently test,
    but don't flip it until it gets to this point. When burgers lift up easily,
    flip, add two slices of cheese to each, close lid if using a grill,
    and cook on the other side for another 2-3 minutes for medium to medium
    rare. Remove burgers with a sturdy metal spatula and transfer to a plate.
    Allow to rest for several minutes, then transfer to buns.
    Garnish as desired and serve immediately.
""",
    user_id=this_user.id,
    cuisine_id=2,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()

recipe = Recipe(
    name="Chocolate Cookies",
    ingredients="""
    1-1/4 cups margarine, softened2 cups white sugar2 eggs,
    3/4 cup unsweetened cocoa powder1 teaspoon baking soda1/8 teaspoon salt,
    2 teaspoons vanilla extract2 cups all-purpose flour,1 cup chopped walnuts
""",
    body="""
    Serving Size-48,Preheat oven to 350 degrees F (175 degrees C).
    In a large bowl, cream together margarine and sugar until smooth. Beat in
    eggs one at a time, then stir in the vanilla. Combine flour, cocoa, baking
    soda, and salt; stir into the creamed mixture until just blended.
    Mix in walnuts. Drop by spoonfuls onto ungreased cookie sheets.
    Bake for 8 to 10 minutes in the preheated oven. Cool for a couple of
    minutes on the cookie sheet before transferring to wire racks to cool
    completely.
""",
    user_id=this_user.id,
    cuisine_id=2,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()

recipe = Recipe(
    name="Chicken Noodles",
    ingredients="""
    4 skinless,boneless chicken breasts
    1 tablespoon vegetable oil
    1/2 cup sliced onion
    2 cups broccoli florets
    2 carrots, julienned
    2 cups snow peas
    4 cups dry Chinese noodles
    1/4 cup teriyaki sauce
""",
    body="""
    Serving Size-4,In a large skillet brown chicken in oil, stirring
    constantly until juices run clear. Add the onion, broccoli, carrots
    and peas. Cover skillet and steam for 2 minutes.
    Add the Chinese noodles and teriyaki sauce.
    Stir noodles into chicken/vegetable mixture,
    making sure they are coated with sauce. When the noodles wilt, serve.
""",
    user_id=this_user.id,
    cuisine_id=3,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()

recipe = Recipe(
    name="Fortune cookies",
    ingredients="""2 large egg whites
    1/2 teaspoon pure vanilla extract
    1/2 teaspoon pure almond extract
    3 tablespoons vegetable oil
    8 tablespoons all-purpose flour
    1 1/2 teaspoons cornstarch
    1/4 teaspoon salt
    8 tablespoons sugar
    3 teaspoons water
""",
    body="""
    Serving Size-10,Write fortunes on pieces of paper that are 3 1/2 inches
    long and 1/2 inch wide. Preheat oven to 300 F. Grease 2 9-X-13 inch baking
    sheets. In a medium bowl, lightly beat the egg white, vanilla extract,
    almond extract, and vegetable oil until frothy, but not stiff. Sift the
    flour, cornstarch, salt, and sugar in a separate bowl. Stir the water into
    the flour mixture.
    Add the flour to the egg white mixture and stir until you have a smooth
    batter.The batter should not be runny but should drop easily off a wooden
    spoon. Note: If you want to dye the fortune cookies, add the food coloring
    at this point, stirring it into the batter. For example, use 1/2 teaspoon
    green food coloring to make green fortune cookies. Place level tablespoons
    of batter onto the cookie sheet, spacing them at least 3 inches apart.
    Gently tilt the baking sheet back and forth and from side to side so that
    each tablespoon of batter forms into a circle 4 inches in diameter.
    Bake until the outer 1/2-inch of each cookie turns golden brown, and they
    are easy to remove from the baking sheet with a spatula (14 to 15 minutes).
    Working quickly, remove the cookie with a spatula and flip it over in your
    hand. Place a fortune in the middle of a cookie.
    To form the fortune cookie shape, fold the cookie in half, then gently pull
    the edges downward over the rim of a glass, wooden spoon or the edge of a
    muffin tin. Place the finished cookie in the cup of the muffin tin so that
    it keeps its shape. Continue with the rest of the cookies.
""",
    user_id=this_user.id,
    cuisine_id=3,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()

recipe = Recipe(
    name="Spaghetti and Meatballs",
    ingredients="""1lb spaghetti,
    1lb ground beef
    1/3cup bread crumbs
    1/4cup finely chopped parsley
    1/4cup freshly grated Parmesan, plus more for serving
    1 egg
    2 garlic cloves, minced
    Kosher salt
    1/2 tsp red pepper flakes
    2 tbsp extra-virgin olive oil
    1/2cup onion, finely chopped
    1 (28-oz) can crushed tomatoes
    1 bay leaf
    Freshly ground black pepper
""",
    body="""
    Serving Size-4,In a large pot of boiling salted water, cook spaghetti
    according to package instructions. Drain. In a large bowl,
    combine beef with bread crumbs, parsley, Parmesan, egg, garlic,
    1 teaspoon salt, and red pepper flakes. Mix until just combined then
    form into 16 balls. In a large pot over medium heat, heat oil.
    Add meatballs and cook, turning occasionally, until browned on all
    sides, about 10 minutes. Transfer meatballs to a plate.
    Add onion to pot and cook until soft, 5 minutes. Add crushed tomatoes
    and bay leaf. Season with salt and pepper and bring to a simmer.
    Return meatballs to pot and cover. Simmer until sauce has thickened,
    8 to 10 minutes. Serve pasta with a healthy scoop of meatballs
    and sauce. Top with Parmesan before serving.
""",
    user_id=this_user.id,
    cuisine_id=4,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()

recipe = Recipe(
    name="Tiramisu",
    ingredients="""
    3 egg whites
    6 egg yolks
    3 tbsp sugar
    8 oz mascarpone cheese at room temperature
    1 cup freshly pulled espresso cooled to room temperature
    2 tbsp amaretto or spiced rum
    3-4 dozen ladyfingers
    cocoa powder for dusting
""",
    body="""
    Serving Size-8,In a clean bowl, whip the egg whites and 3 tbsp of sugar
    together with a hand mixer, for about 3-5 minutes until the egg whites
    hold stiff peaks.

    In a separate bowl, whip the egg yolks with the remaining 3 tbsp sugar
    for 2-3 minutes until the egg yolks are thick and pale yellow in color.
    Add the mascarpone to the egg yolks and whip until combined.
    Gently fold the stiff egg whites into the egg yolk mixture and set aside.
    In a small flat dish or bowl, combine the espresso and amaretto.
    Dunk each ladyfinger into the espresso mixture for 1-2 seconds and place
    into the bottom of a 8x8 dish, or into individual ramekins.
    Do not let the ladyfinger soak so much that it falls apart, just a quick
    dunk to let it absorb a little bit of espresso.
    Once the ladyfingers have formed a single layer in the bottom of the dish,
    spread 1/2 of the mascarpone mixture over the ladyfingers.
    Arrange another layer of espresso soaked ladyfingers on top, and spread
    over the remaining mascarpone cream. Cover the top of the dish with plastic
    wrap and let the tiramisu refrigerate for 4-6 hours.

    Serve cold, with a light dusting of cocoa on top. Enjoy!
""",
    user_id=this_user.id,
    cuisine_id=4,
    created=datetime.datetime.now())
session.add(recipe)
session.commit()
