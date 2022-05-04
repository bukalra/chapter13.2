from flask import Flask
from models import todos, create_table_sql
from flask import redirect, render_template, url_for
from flask import request
from forms import TodoForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

#FORMS responsible functions

@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""

    with todos.create_connection("database.db") as conn:


        if request.method == "POST":
            if form.validate_on_submit():
                updated_fd = form.data
                updated_fd_sql = (updated_fd["title"],updated_fd["description"],updated_fd["done"])
                todos.add_todo(conn, updated_fd_sql)
            return redirect(url_for("todos_list"))

        todos.execute_sql(conn, create_table_sql)
        return render_template("todos.html", form=form, todos=todos.all(conn), error=error)

@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def book_details(todo_id):
   
    with todos.create_connection("database.db") as conn:
        todo = todos.get(conn, todo_id)[0]
        form = TodoForm(data={'title':todo[0], 'description':todo[1], 'done':todo[2]})
        if request.method == "POST":        
            if form.validate_on_submit():
                todos.update(conn, id= todo_id, title=form.data['title'], description=form.data['description'], done=form.data['done'])
            return redirect(url_for("todos_list"))
        return render_template("todo.html", form=form, todo_id=todo_id)

if __name__ == "__main__":
    app.run(debug=True)