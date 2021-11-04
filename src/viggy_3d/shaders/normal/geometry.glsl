# version 330 core


layout (triangles) in;
layout (line_strip, max_vertices = 6) out;


in VS_OUT {
    vec4 normal_pos;
} gs_in[];


void line(int index)
{
    gl_Position = gl_in[index].gl_Position;
    EmitVertex();

    gl_Position = gs_in[index].normal_pos;
    EmitVertex();

    EndPrimitive();
}


void main()
{
    line(0);
    line(1);
    line(2);
}
