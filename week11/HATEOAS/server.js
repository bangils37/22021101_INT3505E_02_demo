const express = require('express');
const hateoasLinker = require('express-hateoas-links');

const app = express();
const PORT = 3000;

// Sử dụng middleware hateoasLinker
app.use(hateoasLinker);

// Dữ liệu giả định
const articles = [
    { id: 1, content: 'HATEOAS example', authorId: 1 },
    { id: 2, content: 'Another HATEOAS example', authorId: 1 },
    { id: 3, content: 'Third article', authorId: 2 }
];

const comments = {
    1: [{ id: 101, text: 'Great article!' }, { id: 102, text: 'Very insightful.' }],
    2: [{ id: 201, text: 'Good read.' }],
    3: []
};

const tags = {
    1: ['HATEOAS', 'REST'],
    2: ['API', 'Design'],
    3: ['Node.js']
};

// Endpoint để lấy danh sách bài viết
app.get('/articles', (req, res) => {
    const articlesWithLinks = articles.map(article => {
        return {
            ...article,
            _links: {
                self: { href: `http://localhost:${PORT}/articles/${article.id}`, rel: 'self', method: 'GET' },
                comments: { href: `http://localhost:${PORT}/articles/${article.id}/comments`, rel: 'comments', method: 'GET' },
                tags: { href: `http://localhost:${PORT}/articles/${article.id}/tags`, rel: 'tags', method: 'GET' }
            }
        };
    });
    res.json(articlesWithLinks);
});

// Endpoint để lấy chi tiết một bài viết
app.get('/articles/:id', (req, res) => {
    const articleId = parseInt(req.params.id);
    const article = articles.find(a => a.id === articleId);

    if (!article) {
        return res.status(404).json({ message: 'Article not found' });
    }

    const articleWithLinks = {
        ...article,
        _links: {
            self: { href: `http://localhost:${PORT}/articles/${article.id}`, rel: 'self', method: 'GET' },
            comments: { href: `http://localhost:${PORT}/articles/${article.id}/comments`, rel: 'comments', method: 'GET' },
            tags: { href: `http://localhost:${PORT}/articles/${article.id}/tags`, rel: 'tags', method: 'GET' }
        }
    };
    res.json(articleWithLinks);
});

// Endpoint để lấy bình luận của một bài viết
app.get('/articles/:id/comments', (req, res) => {
    const articleId = parseInt(req.params.id);
    const articleComments = comments[articleId] || [];
    res.json(articleComments);
});

// Endpoint để lấy tags của một bài viết
app.get('/articles/:id/tags', (req, res) => {
    const articleId = parseInt(req.params.id);
    const articleTags = tags[articleId] || [];
    res.json(articleTags);
});

app.listen(PORT, () => {
    console.log(`HATEOAS Demo API đang chạy tại http://localhost:${PORT}`);
});