class Article:
    # Class variable to keep track of ALL articles (single source of truth)
    _all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        
        self._author = author
        self._magazine = magazine
        
        # Title validation + immutability
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = title
        
        # Store the article
        Article._all.append(self)

    @property
    def title(self):
        return self._title

    # Title should not be changeable after creation
    @title.setter
    def title(self, value):
        if hasattr(self, '_title'):  # already set → prevent change
            raise AttributeError("Cannot change title after creation")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise TypeError("author must be an Author instance")
        self._author = new_author

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if not isinstance(new_magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        self._magazine = new_magazine

    @classmethod
    def all(cls):
        return cls._all


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name cannot be empty")
        self._name = name

    @property
    def name(self):
        return self._name

    # Name should be immutable
    @name.setter
    def name(self, value):
        raise AttributeError("Cannot change name after creation")

    def articles(self):
        return [article for article in Article.all() if article.author is self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        new_article = Article(self, magazine, title)
        return new_article

    def topic_areas(self):
        if not self.articles():
            return None
        return list({mag.category for mag in self.magazines()})


class Magazine:
    # For bonus: top_publisher
    _all = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        
        # Use setters for validation
        self.name = name
        self.category = category
        
        Magazine._all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        if len(value) == 0:
            raise ValueError("Category cannot be empty")
        self._category = value

    def articles(self):
        return [article for article in Article.all() if article.magazine is self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        from collections import Counter
        
        author_count = Counter(article.author for article in self.articles())
        frequent = [author for author, count in author_count.items() if count > 2]
        
        return frequent if frequent else None

    @classmethod
    def top_publisher(cls):
        if not Article.all():
            return None
            
        from collections import Counter
        magazine_count = Counter(article.magazine for article in Article.all())
        
        if not magazine_count:
            return None
            
        return magazine_count.most_common(1)[0][0]