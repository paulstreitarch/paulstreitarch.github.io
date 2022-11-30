# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    #schwarzer hinergrund
    back_color = THREE.Color.new(0.1,0.1,0.1)
    #weißer hinergrund
    #back_color = THREE.Color.new(1.0,1.0,1.0)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 10000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation

    # Create Materials
    global material, line_material, material2  
    color = THREE.Color.new(255,0,0)
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.85
    material.color = color

    line_material = THREE.LineBasicMaterial.new()      
    line_material.color = THREE.Color.new(255,255,255)
    
    #set Parameters
    sphere = []
    spheres = []
    numb = 6
    geom1_params = {
                "radius": 7,
                "widthSegments":12,
                "heightSegments":8
    }
    geom1_params = Object.fromEntries(to_js(geom1_params))

    #generate Geometry
    geom = THREE.SphereGeometry.new(geom1_params.radius, geom1_params.widthSegments, geom1_params.heightSegments)

    for i in range(3,numb+1,1):
        geom2 = geom.clone()
        #Variante1
        geom2.scale(0.1,0.1,0.1)
        geom2.translate(0,i+(i/8),0)
        geom2.scale(1.5*i,1.5*i,1.5*i)
        #Variante2
        """geom2.scale(0.05,0.05,0.05)
        geom2.translate(0,i+(i/2),0)
        geom2.scale(1.5*i*i/2,0.5*i,1.5*i*i/2)"""

        for j in range(0,8,1):
            geom2.rotateZ(math.pi/4)

            for k in range(0,8,1):
                geom2.rotateY(math.pi/4)
                geom3 = geom2.clone()

                color2 = THREE.Color.new(0.02*(i*i),0,1.0-(0.1*i))
                #color2 = THREE.Color.new(0,1.0-(0.1*i),0.02*(i*i))
                material2 = THREE.MeshBasicMaterial.new()
                material2.transparent = True
                material2.opacity = 0.5
                material2.color = color2
                
                # draw mesh
                sphere = THREE.Mesh.new(geom3, material2)
                spheres.append(sphere)
                scene.add(sphere)
                # draw the edge geometrie
                edges = THREE.EdgesGeometry.new(sphere.geometry)
                line = THREE.LineSegments.new(edges, line_material)
                scene.add(line)

    # draw mesh
    sphere = THREE.Mesh.new(geom, material)
    spheres.append(sphere)
    scene.add(sphere)
    # draw the edge geometrie
    edges = THREE.EdgesGeometry.new(sphere.geometry)
    line = THREE.LineSegments.new(edges, line_material)
    scene.add(line)
    

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()