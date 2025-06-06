# app.py
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for

from replacer import TextReplacer

app = Flask(__name__)
app.secret_key = "change_this_to_something_secret"

replacer = TextReplacer()


@app.route("/", methods=["GET", "POST"])
def index():
    replaced_text = None
    error = None

    if request.method == "POST":
        if "add_mapping" in request.form:
            old_word = request.form.get("old_word", "").strip()
            new_word = request.form.get("new_word", "").strip()
            if not old_word:
                error = "يجب إدخال الكلمة القديمة (old word)."
            else:
                replacer.add_replacement(old_word, new_word)
                return redirect(url_for("index"))

        elif "replace_text" in request.form:
            input_text = request.form.get("input_text", "")
            if input_text:
                replaced_text = replacer.replace_text(input_text)
            else:
                error = "لا يوجد نص للاستبدال."
                replaced_text = ""

    return render_template(
        "index.html",
        mappings=replacer.get_mappings(),
        replaced_text=replaced_text,
        error=error
    )


@app.route("/mappings")
def mappings():
    """
    Show the current mapping list (old → new) with delete buttons
    """
    current = replacer.get_mappings()
    return render_template("mappings.html", mappings=current)


@app.route("/delete_mapping", methods=["POST"])
def delete_mapping():
    old_word = request.form.get("old_word_to_delete", "").strip()
    replacer.delete_mapping(old_word)
    return redirect(url_for("mappings"))


if __name__ == "__main__":
    app.run(debug=True)
