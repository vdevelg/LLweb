def index():
    with open(r'./templates/index.html') as template:
        return template.read()


def blog():
    with open(r'./templates/blog.html') as template:
        return template.read()
