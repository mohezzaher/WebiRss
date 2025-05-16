fetch('/api/posts')
  .then(response => response.json())
  .then(posts => {
    const list = document.getElementById('posts');
    posts.forEach(post => {
      const li = document.createElement('li');

      const imageHTML = post.image ? `<img src="${post.image}" alt="Post image">` : '';

      li.innerHTML = `
        ${imageHTML}
        <div class="post-content">
          <a href="${post.link}" target="_blank">${post.title}</a>
          <p>${post.summary}...</p>
          <small>${post.source} — ${new Date(post.pubDate).toLocaleString()}</small>
        </div>
      `;
      list.appendChild(li);
    });
  })
  .catch(err => {
    console.error('Failed to fetch posts:', err);
  });
