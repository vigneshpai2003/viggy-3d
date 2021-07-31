# version 330 core

layout (location = 0) in vec3 position;

out vec3 vs_UV;

uniform mat4 view;
uniform mat4 projection;


void main()
{
    // remove all translation from view matrix using mat3 conversion
    gl_Position = projection * mat4(mat3(view)) * vec4(position, 1.0);
    vs_UV = position;
}
