# Import javascript modules
from js import THREE, window, document, Object, console
from pyodide.ffi import create_proxy, to_js
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
    camera.position.z = 75
    camera.position.y = 45
    camera.position.x = 30
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

   
    
    #set Parameters
    global innerSphere, iLine, outerSphere, oLine, spheres, geom1_params, lines,farb, r, g, b

    innerSphere = []
    outerSphere = []
    spheres = []
    lines = []

    geom1_params = {
                "radius": 7,
                "widthSegments":12,
                "heightSegments":8,
                "numb":6,
                "color": THREE.Color.new("rgb(255,0,0)"),
                "colorline": THREE.Color.new("rgb(255,255,255)"),
                "colorlol": 1.00,
                "animate": animate,
                "stop": stop
                
                
    }
    geom1_params = Object.fromEntries(to_js(geom1_params))

    farb = geom1_params.colorlol

    # Create Materials
    global material, line_material, material2  
    color = geom1_params.color
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.85
    material.color = color

    linecolor = geom1_params.colorline
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = linecolor

    #set up gui

    global spheres_radius, spheres_number, x, folder1
    x = 0

    gui = window.lil.GUI.new()

    gui.addColor(geom1_params, 'color').name('color of the core')
    
    gui.addColor(geom1_params, 'colorline').name('color of the lines')

    folder1 = gui.addFolder('color gradient')
    folder1.add(geom1_params, 'colorlol',0.00,5.00,0.25).name('factor')

    gui.add(geom1_params, 'animate').name('let it roll !')
    gui.add(geom1_params, 'stop').name('stop it !')

    gui.title('transform them !')

    spheres_radius = geom1_params.radius
    spheres_number = geom1_params.numb

    #generate Geometry
    spheresfun()

    # draw mesh
    innerSphere = THREE.Mesh.new(geom, material)
    #spheres.append(innerSphere)
    scene.add(innerSphere)
    # draw the edge geometrie
    iEdges = THREE.EdgesGeometry.new(innerSphere.geometry)
    iLine = THREE.LineSegments.new(iEdges, line_material)
    scene.add(iLine)

    #console.log(outerSphere)
    

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    controls.damping = 0.2
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS

def spheresfun():
    global geom, geom2, geom3, oLine, farb, farb1

    geom = THREE.SphereGeometry.new(geom1_params.radius, geom1_params.widthSegments, geom1_params.heightSegments)

    for i in range(3,geom1_params.numb+1,1):
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

                r = 0.02
                g = 0
                b = 0.1

                geom2.rotateY(math.pi/4)
                geom3 = geom2.clone()

                farb1 = farb/10

                color2 = THREE.Color.new(r*(i*i)*farb,g,1.0-(b*i)*farb)
                #color2 = THREE.Color.new(0.02*(i*i),0,1.0-(0.1*i))
                #color2 = THREE.Color.new(0,1.0-(0.1*i),0.02*(i*i))
                material2 = THREE.MeshBasicMaterial.new()
                material2.transparent = True
                material2.opacity = 0.5
                material2.color = color2
                
                # draw mesh
                outerSphere = THREE.Mesh.new(geom3, material2)
                #innerSphere.append(outerSphere)
                spheres.append(outerSphere)
                scene.add(outerSphere)
                # draw the edge geometrie
                oEdges = THREE.EdgesGeometry.new(outerSphere.geometry)
                oLine = THREE.LineSegments.new(oEdges, line_material)
                lines.append(oLine)
                scene.add(oLine)



# Simple render and animate

def update():
    global outerSphere, farb
    
    if farb != geom1_params.colorlol:
        
        farb = geom1_params.colorlol
        
        for outerSphere in spheres:
            spheres.clear
            lines.clear
            
            scene.remove(oLine)
            scene.remove(outerSphere)

        spheresfun()
    

    


def render(*args):
    update()
    rotate()

    window.requestAnimationFrame(create_proxy(render))
    renderer.setAnimationLoop(animate)
    controls.update()
    composer.render()

def animate():
    global x
    if x != 1:
        x = 1

    for outerSphere in spheres:
            scene.remove(outerSphere)
            spheres.clear
    for oLine in lines:
            scene.remove(oLine)
            lines.clear

def stop():
    global x
    if x == 1:
        x = 0
    
    spheresfun()

    

def rotate():
    global x, outerSphere, oLine, lines

    if x == 1:
        sphereRot = 0.008
        innerSphere.rotateY(sphereRot)
        iLine.rotateY(sphereRot)
        
        
            
        
            

        
        


    




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