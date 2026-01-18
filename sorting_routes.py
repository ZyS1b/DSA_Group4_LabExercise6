from flask import Blueprint, render_template

sorting_blueprint = Blueprint('sorting_blueprint', __name__)

@sorting_blueprint.route('/works/sorting')
def sorting_page():
    return render_template("sorting.html", site_name="Nodeus", page_class="theme-sorting")