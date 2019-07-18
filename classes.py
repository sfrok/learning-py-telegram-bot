from datetime import date


class Document:
    def __init__(self, title='', number=0, doc_date=date.today(), content='', doc=None):
        self.__title = title
        self.number = number
        self.doc_date = doc_date
        self.content = content
        if doc is not None:
            self.__title = doc.title
            self.number = doc.number
            self.doc_date = doc.doc_date
            self.content = doc.content
            if title is not '':
                self.__title = title
            if number is not 0:
                self.number = number
            if doc_date is not date.today():
                self.doc_date = doc_date
            if content is not '':
                self.content = content

    def __del__(self):
        pass

    def display_info(self):
        return f"Doc. #{self.number} as of {self.doc_date} - '{self.__title}'"

    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title


class Journal(Document):
    def __init__(self, title='', number=0, doc_date=date.today(), content=[], doc=None):
        super().__init__(title, number, doc_date, content, doc)
        self.__title = title
        self.number = number
        self.doc_date = doc_date
        self.content = content
        if doc is not None:
            self.__title = doc.title
            self.number = doc.number
            self.doc_date = doc.doc_date
            self.content = doc.content
            if title is not '':
                self.__title = title
            if number is not 0:
                self.number = number
            if doc_date is not date.today():
                self.doc_date = doc_date
            if content is not '':
                self.content = content
