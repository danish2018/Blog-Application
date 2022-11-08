
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from . import db
from .models import Post,User,Comment,Like
from datetime import datetime
import pytz

t = pytz.timezone('Asia/Kolkata')



show = Blueprint('show',__name__)

@show.route("/")
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', user = current_user, posts = posts)



@show.route("/create-post",methods = ["GET","POST"])
@login_required
def create_post():
    if request.method =="POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty',category = 'error')
        else:
            post = Post(text=text, author=current_user.id, date_created = datetime.now(t).strftime('%d-%m-%Y %H:%M:%S'))
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('show.index'))
    return render_template('create-post.html',user = current_user)



@show.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash("Post does not exist", category = "error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post", category = 'error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted",category= 'success')
    return redirect(url_for('show.index'))

@show.route("/#update-post/<id>",methods = ["GET","POST"])
@login_required
def update_post(id):
    post_update = Post.query.filter_by(id = id).first()

    if request.method == 'POST':
        post_update.text = request.form.get('text')
        db.session.commit()
        flash("Post updated",category= 'success')
        return redirect(url_for('show.index'))
    return render_template('updatepost.html',user = current_user,post = post_update)

    # if not post:
    #     flash("Post does not exist", category = "error")
    # elif current_user.id != post.author:
    #     flash("You do not have permission to delete this post", category = 'error')
    # else:
    #     db.session.delete(post)
    #     db.session.commit()
    #     flash("Post deleted",category= 'success')
    # return redirect(url_for('show.index'))



@show.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username= username).first()
    if not user:
        flash('No user exist with this name', category='error')
        return redirect(url_for('show.index'))
    posts = user.posts
    return render_template("posts.html",user = current_user, posts = posts,username = username)



@show.route("/create-comment/<post_id>",methods = ["GET","POST"])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    

    if not text:
        flash('Comment can not be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text = text ,author=current_user.id,post_id=post_id,date_created = datetime.now(t).strftime('%d-%m-%Y %H:%M:%S'))
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist')
    return redirect (url_for('show.index'))



@show.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist',category = 'error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You don't have permission to delete this comment",category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('show.index'))



@show.route("/user-profile")
@login_required
def user_profile():

    return render_template('userprofile.html',user = current_user)



@show.route("/update-profile",methods = ["GET","POST"])
@login_required
def update_profile():
    my_data = User.query.filter_by(id=current_user.id).first()
    data = request.form
    if request.method == 'POST':
        my_data.username= data.get("username")
        my_data.contact= data.get("contact")
        db.session.commit()
        return redirect(url_for('show.user_profile'))
    return render_template('updateprofile.html',user = current_user)


@show.route("/like-post/<post_id>",methods = ["GET"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(author=current_user.id,post_id=post_id).first()

    if not post:
        flash('Post does not exist',category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like =  Like(author = current_user.id , post_id=post_id,date_created = datetime.now(t).strftime('%d-%m-%Y %H:%M:%S'))
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('show.index'))



@show.route("/post/<id>",methods = ["GET","POST"])
def check(id):
    post_update = Post.query.filter_by(id = id).first()

    if request.method == 'POST':
        post_update.text = request.form.get('text')
        db.session.commit()
        flash("Post updated",category= 'success')
        return redirect(url_for('show.index'))

