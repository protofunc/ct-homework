from flask import render_template, request, flash, redirect, url_for
from app.blueprints.posts.forms import PostForm
from app.blueprints.posts import posts
from app.models import Post
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required
from app.models import Post, User

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

#Dynamic Routes

'''View single post'''
@posts.route('/<int:post_id>', methods=['GET'])
@login_required
def view_single_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('view_single_post.html', post=post)
    else:
        flash('This post does not exist.', 'danger')
        return redirect(url_for('posts.view_post.html'))

@posts.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        if request.method == 'POST' and form.validate_on_submit():

            # Grabbing our form data and storing into a dict
            new_post_data = {
                'img_url': form.img_url.data,
                'title': form.title.data.title(),
                'caption': form.caption.data,
                'user_id': current_user.id
            }

            # Implementing values from our form data for our instance
            post.from_dict(new_post_data)

            # Update post to database
            post.update_to_db()

            flash('You have successfully updated your post!', 'success')
            return redirect(url_for('posts.view_post'))
    return render_template('update_post.html', form=form, post=post)

# Delete posts
@posts.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        post.delete_post()
    else:
        flash('You do not have permissions to delete this post.', 'danger')
    return redirect(url_for('posts.view_post'))

# Follow users
@posts.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.follow_user(user)
        flash(f'Successfully followed {user.first_name}!', 'success')
    return redirect(url_for('main.home'))

# unfollow route
@posts.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.unfollow_user(user)
        flash(f'You are no longer following {user.first_name}!', 'warning')
    return redirect(url_for('main.home'))