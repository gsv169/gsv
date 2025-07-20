// Studio environment generator for realistic jewelry rendering
export function createStudioEnvironment(renderer) {
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    pmremGenerator.compileEquirectangularShader();
    
    // Create a simple studio environment texture
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    
    // Create gradient for studio lighting
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, '#ffffff');
    gradient.addColorStop(0.3, '#f0f0f0');
    gradient.addColorStop(0.5, '#e0e0e0');
    gradient.addColorStop(0.7, '#d0d0d0');
    gradient.addColorStop(1, '#c0c0c0');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Add some bright spots for reflections
    const addLightSpot = (x, y, radius, intensity) => {
        const spotGradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
        spotGradient.addColorStop(0, `rgba(255, 255, 255, ${intensity})`);
        spotGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = spotGradient;
        ctx.fillRect(x - radius, y - radius, radius * 2, radius * 2);
    };
    
    // Add multiple light sources
    addLightSpot(100, 50, 40, 0.8);
    addLightSpot(300, 80, 60, 0.6);
    addLightSpot(450, 40, 30, 0.7);
    addLightSpot(200, 150, 50, 0.5);
    
    // Create texture from canvas
    const texture = new THREE.CanvasTexture(canvas);
    texture.mapping = THREE.EquirectangularReflectionMapping;
    texture.encoding = THREE.sRGBEncoding;
    
    const envMap = pmremGenerator.fromEquirectangular(texture).texture;
    pmremGenerator.dispose();
    
    return envMap;
}