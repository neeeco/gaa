
    let allResults = [], allFixtures = [];

    // fetch both JSON files
    Promise.all([
      fetch('results.json').then(r => r.json()),
      fetch('fixtures.json').then(r => r.json())
    ]).then(([results, fixtures]) => {
      allResults = results;
      allFixtures = fixtures;

      // date
      fetch('fixtures.json')
        .then(response => response.json())
        .then(data => {
          // Sort fixtures by date (soonest first)
          data.sort((a, b) => new Date(a.date) - new Date(b.date));

          // Now render them (replace this with your rendering logic)
          data.forEach(match => {
            // Example rendering logic
            const matchDiv = document.createElement('div');
            matchDiv.innerHTML = `
        <div class="match-header">
          <span>${match.team_1} vs ${match.team_2}</span>
          <span class="match-date">${new Date(match.date).toLocaleDateString()}</span>
        </div>
        <div class="match-meta">${match.venue} | ${match.referee}</div>
      `;
            document.getElementById('fixtures-container').appendChild(matchDiv);
          });
        });


      const gamesInResults = [...new Set(allResults.map(m => m.game))];
      const gamesInFixtures = [...new Set(allFixtures.map(m => m.game))];

      // ───── Sort by date ─────
      allResults.sort((a, b) => new Date(b.date) - new Date(a.date));   // newest first
      allFixtures.sort((a, b) => new Date(a.date) - new Date(b.date));  // earliest first

      renderMatches();  // initial render of everything
    });

    // 3. Paste your filter-listening code right here:
    const gameFilter = document.getElementById('gameFilter');
    gameFilter.addEventListener('change', () => {
      renderMatches();
    });

    // 4. renderMatches uses the dropdown value to filter
    function renderMatches() {
      const filter = gameFilter.value.toLowerCase();
      const resultsEl = document.getElementById('results');
      const fixturesEl = document.getElementById('fixtures');
      resultsEl.innerHTML = '';
      fixturesEl.innerHTML = '';

      const filteredResults = filter === 'all'
        ? allResults
        : allResults.filter(m => (m.game || '').toLowerCase() === filter);

      const filteredFixtures = filter === 'all'
        ? allFixtures
        : allFixtures.filter(m => (m.game || '').toLowerCase() === filter);

      filteredResults.forEach(m => {
        const li = document.createElement('li');
        li.innerHTML = `
          <div class="match-header">
            <span class="match-date">${new Date(m.date).toLocaleDateString()}</span>
            <strong>${m.team_1}</strong> 
            <span class="score">${m.score_1}</span> vs 
            <span class="score">${m.score_2}</span> 
            <strong>${m.team_2}</strong>
          </div>
         <div class="match-meta">
            ${m.venue}
          </div>
        `;
        resultsEl.appendChild(li);
      });

      filteredFixtures.forEach(m => {
        const li = document.createElement('li');
        li.innerHTML = `
          <div class="match-header">
            <span class="match-date">${new Date(m.date).toLocaleDateString()}</span>
            <strong>${m.team_1}</strong> vs <strong>${m.team_2}</strong>
          </div>
          <div class="match-meta">
            ${m.venue}
          </div>
        `;
        fixturesEl.appendChild(li);
      });
    }

