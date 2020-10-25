def index():
    with open(r'D:/proj/LLweb/templates/index.html') as template:
        return template.read()


def blog():
    with open(r'D:/proj/LLweb/templates/blog.html') as template:
        return template.read()
