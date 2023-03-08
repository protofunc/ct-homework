from flask import render_template, request, flash, redirect, url_for
from app.blueprints.posts.forms import PostForm
from app.blueprints.posts import posts
from app.models import Post
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required

'''Registration route'''
@posts.route('/create_post', methods = ['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Grabbing our form data and storing into a dict
        new_post_data = {
            'img_url': form.img_url.data,
            'title': form.title.data,
            'caption': form.caption.data,
            'user_id': current_user.id
        }

        # Create instance of User
        new_post = Post()

        # Implementing values from our form data for our instance
        new_post.from_dict(new_post_data)

        # Save user to database
        new_post.save_to_db()

        flash('You have successfully posted!', 'success')
        return redirect(url_for('posts.view_post'))
    return render_template('create_post.html', form=form)

'''View post route'''
@posts.route('/logout', methods=['GET'])
@login_required
def view_post():
    posts = Post.query.all()
    return render_template('view_post.html', posts=posts)