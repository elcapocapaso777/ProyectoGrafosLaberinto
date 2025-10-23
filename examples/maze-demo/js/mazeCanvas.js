// createMazeRenderer(canvasEl)
// Uso: const r = createMazeRenderer(canvasEl); r.render(maze, options); r.animatePath(path, opts);
function createMazeRenderer(canvas) {
  const ctx = canvas.getContext('2d', { alpha: true });
  const dpr = window.devicePixelRatio || 1;

  function resize(width, height) {
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function roundRectPath(x, y, w, h, r) {
    ctx.beginPath();
    const radius = Math.min(r, w/2, h/2);
    ctx.moveTo(x + radius, y);
    ctx.arcTo(x + w, y, x + w, y + h, radius);
    ctx.arcTo(x + w, y + h, x, y + h, radius);
    ctx.arcTo(x, y + h, x, y, radius);
    ctx.arcTo(x, y, x + w, y, radius);
    ctx.closePath();
  }

  // Genera un patrón sutil para "textura" del muro
  function createWallPattern(intensity = 0.5) {
    const p = document.createElement('canvas');
    p.width = 64; p.height = 64;
    const pc = p.getContext('2d');
    // base ligera
    pc.fillStyle = '#e6e6e6';
    pc.fillRect(0,0,64,64);
    // motas sutiles
    pc.fillStyle = 'rgba(0,0,0,' + (0.04 * intensity) + ')';
    for (let i=0;i<20;i++){
      const x = Math.random()*64, y = Math.random()*64, w = Math.random()*6+1, h= Math.random()*1.5;
      pc.fillRect(x,y,w,h);
    }
    // líneas finas
    pc.strokeStyle = 'rgba(255,255,255,0.03)';
    pc.lineWidth = 0.6;
    for (let i=0;i<6;i++){
      const yy = Math.random()*64;
      pc.beginPath(); pc.moveTo(0,yy); pc.lineTo(64,yy); pc.stroke();
    }
    return ctx.createPattern(p, 'repeat');
  }

  function drawBackground(width, height) {
    const g = ctx.createLinearGradient(0,0,0,height);
    g.addColorStop(0, '#0b1220');
    g.addColorStop(1, '#0f1724');
    ctx.fillStyle = g;
    ctx.fillRect(0,0,width,height);
  }

  // Dibuja el suelo (baldosa sutil)
  function drawGridFloor(maze, opt) {
    const rows = maze.rows, cols = maze.cols, cell = opt.cellSize;
    const w = cols * cell, h = rows * cell;
    const grd = ctx.createLinearGradient(0,0,0,h);
    grd.addColorStop(0, '#0f1724');
    grd.addColorStop(1, '#0b1220');
    ctx.fillStyle = grd;
    ctx.fillRect(0,0,w,h);

    // ligeras líneas de baldosas
    ctx.save();
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(255,255,255,0.02)';
    for (let r=1;r<rows;r++){
      ctx.beginPath(); ctx.moveTo(0, r*cell); ctx.lineTo(w, r*cell); ctx.stroke();
    }
    for (let c=1;c<cols;c++){
      ctx.beginPath(); ctx.moveTo(c*cell, 0); ctx.lineTo(c*cell, h); ctx.stroke();
    }
    ctx.restore();
  }

  // Dibuja las paredes con esquinas redondeadas y "uniones" en esquinas
  function drawWalls(maze, opt) {
    const rows = maze.rows, cols = maze.cols;
    const cell = opt.cellSize, wt = opt.wallThickness, radius = Math.max(3, wt*0.6);
    const pattern = createWallPattern(opt.textureIntensity || 0.6);

    ctx.save();
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    for (let r=0;r<rows;r++){
      for (let c=0;c<cols;c++){ 
        const cellObj = maze.cells[r][c];
        const x = c*cell, y = r*cell;

        // Top
        if (cellObj.walls.top) {
          const wx = x - wt/2, wy = y - wt/2, ww = cell + wt, wh = wt;
          ctx.save();
          ctx.fillStyle = pattern;
          ctx.shadowColor = 'rgba(0,0,0,0.55)';
          ctx.shadowBlur = 10;
          roundRectPath(wx, wy, ww, wh, radius);
          ctx.fill();
          ctx.lineWidth = 1;
          ctx.strokeStyle = 'rgba(0,0,0,0.25)';
          ctx.stroke();
          ctx.restore();
        }
        // Right
        if (cellObj.walls.right) {
          const wx = x + cell - wt/2, wy = y - wt/2, ww = wt, wh = cell + wt;
          ctx.save();
          ctx.fillStyle = pattern;
          ctx.shadowColor = 'rgba(0,0,0,0.55)';
          ctx.shadowBlur = 10;
          roundRectPath(wx, wy, ww, wh, radius);
          ctx.fill();
          ctx.lineWidth = 1;
          ctx.strokeStyle = 'rgba(0,0,0,0.25)';
          ctx.stroke();
          ctx.restore();
        }
        // Bottom
        if (cellObj.walls.bottom) {
          const wx = x - wt/2, wy = y + cell - wt/2, ww = cell + wt, wh = wt;
          ctx.save();
          ctx.fillStyle = pattern;
          ctx.shadowColor = 'rgba(0,0,0,0.55)';
          ctx.shadowBlur = 10;
          roundRectPath(wx, wy, ww, wh, radius);
          ctx.fill();
          ctx.lineWidth = 1;
          ctx.strokeStyle = 'rgba(0,0,0,0.25)';
          ctx.stroke();
          ctx.restore();
        }
        // Left
        if (cellObj.walls.left) {
          const wx = x - wt/2, wy = y - wt/2, ww = wt, wh = cell + wt;
          ctx.save();
          ctx.fillStyle = pattern;
          ctx.shadowColor = 'rgba(0,0,0,0.55)';
          ctx.shadowBlur = 10;
          roundRectPath(wx, wy, ww, wh, radius);
          ctx.fill();
          ctx.lineWidth = 1;
          ctx.strokeStyle = 'rgba(0,0,0,0.25)';
          ctx.stroke();
          ctx.restore();
        }

        // Uniones en esquinas (pequeños circulos) para suavizar
        const top = cellObj.walls.top, left = cellObj.walls.left, right = cellObj.walls.right, bottom = cellObj.walls.bottom;
        const cornerRadius = Math.max(2, radius/2);
        ctx.save();
        ctx.fillStyle = '#dcdcdc';
        ctx.globalAlpha = 0.95;
        ctx.shadowColor = 'rgba(0,0,0,0.35)';
        ctx.shadowBlur = 6;
        // top-left
        if (top && left) {
          ctx.beginPath(); ctx.arc(x, y, cornerRadius, 0, Math.PI*2); ctx.fill();
        }
        // top-right
        if (top && right) {
          ctx.beginPath(); ctx.arc(x+cell, y, cornerRadius, 0, Math.PI*2); ctx.fill();
        }
        // bottom-left
        if (bottom && left) {
          ctx.beginPath(); ctx.arc(x, y+cell, cornerRadius, 0, Math.PI*2); ctx.fill();
        }
        // bottom-right
        if (bottom && right) {
          ctx.beginPath(); ctx.arc(x+cell, y+cell, cornerRadius, 0, Math.PI*2); ctx.fill();
        }
        ctx.restore();
      }
    }
    ctx.restore();
  }

  // Dibuja la solución (estático) con glow
  function drawPath(path, maze, opt) {
    const cell = opt.cellSize;
    ctx.save();
    ctx.lineWidth = Math.max(6, opt.cellSize * 0.12);
    const grad = ctx.createLinearGradient(0, 0, maze.cols*cell, maze.rows*cell);
    grad.addColorStop(0, '#ffd65b');
    grad.addColorStop(1, '#ff8a00');
    ctx.strokeStyle = grad;
    ctx.shadowColor = 'rgba(255,170,50,0.85)';
    ctx.shadowBlur = 18;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    ctx.beginPath();
    path.forEach((p, i) => {
      const cx = p.c * cell + cell/2;
      const cy = p.r * cell + cell/2;
      if (i===0) ctx.moveTo(cx, cy); else ctx.lineTo(cx, cy);
    });
    ctx.stroke();
    ctx.restore();
  }

  // Animar el trazado del path con 'pulse' glow
  function animatePath(path, maze, opts = {}) {
    const duration = opts.duration || 2200;
    const opt = Object.assign({ cellSize: opts.cellSize || 60, wallThickness: opts.wallThickness || 10 }, opts);
    const total = path.length;
    let start = null;

    // Precompute points
    const points = path.map(p => ({ x: p.c * opt.cellSize + opt.cellSize/2, y: p.r * opt.cellSize + opt.cellSize/2 }));

    function step(ts) {
      if (!start) start = ts;
      const t = Math.min(1, (ts - start) / duration);
      const upto = Math.floor(t * (total - 1));

      // Redibujar laberinto base (asegura fondo + muros)
      render(maze, opt);

      // dibujar trazo parcial con pulso
      ctx.save();
      const progress = (t * (total - 1)) % (total - 1);
      ctx.lineWidth = Math.max(6, opt.cellSize * 0.12);
      // trazo principal
      ctx.strokeStyle = '#ffd65b';
      ctx.shadowColor = 'rgba(255,170,50,0.95)';
      ctx.shadowBlur = 16 + 10 * Math.sin(t * Math.PI * 2); // pulso
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      ctx.beginPath();
      for (let i = 0; i <= upto; i++) {
        const pt = points[i];
        if (i === 0) ctx.moveTo(pt.x, pt.y); else ctx.lineTo(pt.x, pt.y);
      }
      // segmento parcial hacia el siguiente punto
      if (upto < points.length - 1) {
        const a = points[upto];
        const b = points[upto + 1];
        const segT = (t * (total - 1)) - upto;
        const ix = a.x + (b.x - a.x) * segT;
        const iy = a.y + (b.y - a.y) * segT;
        ctx.lineTo(ix, iy);
      }
      ctx.stroke();
      ctx.restore();

      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // Render principal
  function render(maze, options = {}) {
    const opt = Object.assign({
      cellSize: 60,
      wallThickness: 10,
      textureIntensity: 0.6,
      path: null
    }, options);

    const width = maze.cols * opt.cellSize;
    const height = maze.rows * opt.cellSize;
    resize(width, height);

    ctx.clearRect(0,0,canvas.width, canvas.height);
    drawBackground(width, height);
    drawGridFloor(maze, opt);
    drawWalls(maze, opt);

    if (opt.path && opt.path.length) {
      drawPath(opt.path, maze, opt);
    }
  }

  return {
    render,
    animatePath,
    resize
  };
}

// Exponer globalmente si se importa via <script>
if (typeof window !== 'undefined') window.createMazeRenderer = createMazeRenderer;
