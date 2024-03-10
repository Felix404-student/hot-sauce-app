from app.hotsauces import bp
from app.extensions import db
from app.models.hotsauce import HotSauce, Rating
from app.forms import HotSauceForm, RateHotSauceForm
from flask import render_template, redirect, url_for, flash, session, abort


def format_bottle_style(bottle_style):
    # Replace spaces with hyphens and append '.png'
    return '-'.join(bottle_style.split()).lower() + '.png'

@bp.route("/")
def show_all_hot_sauces():
    """Return a list of hot sauces."""

    all_hotsauces = HotSauce.query.all()
    # Calculate average ratings for each hot sauce
    average_ratings = {}
    for hot_sauce in all_hotsauces:
        ratings = Rating.query.filter_by(hotsauce_id=hot_sauce.id).all()
        if ratings:
            total_flavor = sum(rating.flavor for rating in ratings)
            total_heat = sum(rating.heat for rating in ratings)
            average_flavor = total_flavor / len(ratings)
            average_heat = total_heat / len(ratings)
            average_ratings[hot_sauce.id] = {
                'image_filename': format_bottle_style(hot_sauce.bottle),
                'flavor': average_flavor,
                'heat': average_heat
            }
        else:
            average_ratings[hot_sauce.id] = {
                'image_filename': format_bottle_style(hot_sauce.bottle),
                'flavor': 5,
                'heat': 5
            }

    return render_template('hotsauces/all_hotsauces.html', title='Hot Sauces', hotsauces=all_hotsauces,
                           average_ratings=average_ratings)


@bp.route("/add", methods=['GET', 'POST'])
def add_hot_sauce():
    form = HotSauceForm()
    if form.validate_on_submit():
        hot_sauce = HotSauce(
            name=form.name.data,
            base=form.base.data,
            pepper=form.pepper.data,
            bottle=form.bottle.data
        )
        db.session.add(hot_sauce)
        db.session.commit()
        flash('Hot sauce added successfully!', 'success')
        return redirect(url_for('hotsauces.show_all_hot_sauces'))  # Redirect to the list of hot sauces
    return render_template("hotsauces/new_hotsauce.html", title='Add Hot Sauce', form=form)


@bp.route("/rate", methods=["GET", "POST"])
def rate_hotsauce():
    """Rate a Hot Sauce."""
    form = RateHotSauceForm()

    # Retrieve hot sauces not already rated by the user
    rated_hotsauces = Rating.query.filter_by(user_id=session.get("user_id")).all()
    unrated_hotsauces = HotSauce.query.filter(HotSauce.id.notin_([rating.hotsauce_id for rating in rated_hotsauces])).all()
    form.hotsauce.choices = [(hotsauce.id, hotsauce.name) for hotsauce in unrated_hotsauces]

    if form.validate_on_submit():
        hotsauce_id = form.hotsauce.data
        flavor = form.flavor.data
        heat = form.heat.data

        # Check if the user has already rated this hot sauce
        existing_rating = Rating.query.filter_by(user_id=session.get("user_id"), hotsauce_id=hotsauce_id).first()
        if existing_rating:
            flash('You have already rated this hot sauce.', 'warning')
            return redirect(url_for('rate_hotsauce'))

        new_rating = Rating(hotsauce_id=hotsauce_id, user_id=session.get("user_id"), flavor=flavor, heat=heat)
        db.session.add(new_rating)
        db.session.commit()
        flash('Hot sauce rated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template("hotsauces/rate_hotsauce.html", form=form)


@bp.route("/<int:hotsauce_id>")
def hotsauce_details(hotsauce_id):
    # Retrieve the hot sauce from the database
    hot_sauce = HotSauce.query.get(hotsauce_id)

    if hot_sauce:
        # Render a template to display the hot sauce details
        image =  {
            'filename': format_bottle_style(hot_sauce.bottle)
            }
        return render_template('hotsauces/hotsauce.html', title='Hot Sauce Details', hotsauce=hot_sauce, image=image)
    else:
        # If the hot sauce does not exist, return a 404 error
        abort(404)
