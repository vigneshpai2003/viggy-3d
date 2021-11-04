# version 330 core


layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 i_position;


out VS_OUT {
    vec4 normal_pos;
} vs_out;


uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float size;


void main()
{
    gl_Position = projection * view * (model * vec4(position, 1.0) + vec4(i_position, 0.0));
    vs_out.normal_pos = gl_Position + projection * view * model * vec4(size * normal, 0.0);
}
