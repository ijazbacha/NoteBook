from app import app, db
from flask import Flask, render_template, redirect, url_for, request, flash
from app.models import AddNote
from werkzeug.utils import secure_filename
import os


app.config["IMAGE_UPLOADS"] = os.path.join(app.root_path, 'static')

@app.route('/')
def index():
    notes = AddNote.query.all()
    return render_template('index.html', title='NoteBook', notes=notes)

@app.route('/note_details/<id>')
def note_details(id):
    note = AddNote.query.filter_by(id=id).first()
    return render_template('note_details.html', title='Details Notes', note=note)


@app.route('/create_note', methods=['POST', 'GET'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        img = request.files['img']


        if img.filename == '':
            return 'Please upload image', 400
        
        img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

        file_name = secure_filename(img.filename)
        data = AddNote(title=title, description=description, img_name=file_name, img=img.read())
        db.session.add(data)
        db.session.commit()
        flash('Note is been successfully added')
        return redirect(url_for('index'))
        
    return render_template('note.html', title='Add Notes', note=None)


@app.route('/update_note/<id>', methods=['POST', 'GET'])
def update_note(id):
    note = AddNote.query.filter_by(id=id).first()
    try:
        if request.method == 'POST':
            note.title = request.form['title'] 
            note.description = request.form['description']
            img = request.files['img']
            if img:

                if img.filename == '':
                    return 'Please upload image', 400

                img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))
                file_name = secure_filename(img.filename)
                img=img.read()
                note.img = img
                note.img_name = file_name
            
            
            db.session.commit()
            flash('Your note has been update!')
            return redirect(url_for('index'))
    except:
        pass
    return render_template('note.html', title='Update Note', note=note)


@app.route('/delete_note/<id>')
def delete_note(id):
    note = AddNote.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!')
    return redirect(url_for('index'))
