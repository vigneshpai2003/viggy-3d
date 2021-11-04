# version 330 core

in vec3 vs_UV;

uniform samplerCube texture_cube_map;


void main()
{
    gl_FragColor = texture(texture_cube_map, vs_UV);
}
