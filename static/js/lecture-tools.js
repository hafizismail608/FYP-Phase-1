/* Global lecture tools */
(function(){
  function disable(el, v){ if (el) el.disabled = v; }

  window.generateSubs = async function(url, btnId){
    const btn = btnId ? document.getElementById(btnId) : null;
    disable(btn, true);
    try {
      const resp = await fetch(url, { method: 'POST', credentials: 'same-origin' });
      if (!resp.ok) {
        const txt = await resp.text();
        alert('Subtitle generation failed: ' + resp.status + ' ' + txt);
        return;
      }
      const data = await resp.json();
      if (data && data.status === 'success') { location.reload(); }
      else { alert('Subtitle generation failed'); }
    } catch (e) {
      alert('Subtitle generation error');
    } finally {
      disable(btn, false);
    }
  };

  window.generateDub = async function(url, btnId){
    const btn = btnId ? document.getElementById(btnId) : null;
    disable(btn, true);
    try {
      const resp = await fetch(url, { method: 'POST', credentials: 'same-origin' });
      if (!resp.ok) {
        const txt = await resp.text();
        alert('Dubbing failed: ' + resp.status + ' ' + txt);
        return;
      }
      const data = await resp.json();
      if (data && data.status === 'success') { location.reload(); }
      else { alert('Dubbing failed'); }
    } catch (e) {
      alert('Dubbing error');
    } finally {
      disable(btn, false);
    }
  };

  window.toggleDub = function(originalUrl, dubbedUrl, videoId, sourceId){
    const video = document.getElementById(videoId || 'lecture-video');
    const source = document.getElementById(sourceId || 'videoSource');
    if (!video || !source) return;
    const useDub = !(source.src && source.src.endsWith(dubbedUrl));
    source.src = useDub ? dubbedUrl : originalUrl;
    video.load();
    video.play();
  };
})();
