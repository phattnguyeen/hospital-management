import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

export function initThreeScene(container: HTMLElement) {
  // Scene
  const scene = new THREE.Scene();

  // Camera
  const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.z = 5;

  // Renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  // Load the GLTF model
  const loader = new GLTFLoader();
  loader.load('assets/img/doctor-day.glb', (gltf) => {
    const model = gltf.scene;
    model.scale.set(1, 1, 1); // Adjust the scale if necessary
    scene.add(model);

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      model.rotation.y += 0.01; // Rotate the model for a simple animation
      renderer.render(scene, camera);
    }

    animate();
  }, undefined, (error) => {
    console.error('An error happened while loading the model', error);
  });

  // Handle window resize
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
}