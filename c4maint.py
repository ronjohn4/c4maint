from app import create_app, db
from app.models import Parent, Member

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Account': Parent, 'Member': Member}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # app.run(port=5000, debug=False)
