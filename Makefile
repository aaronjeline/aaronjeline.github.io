
all: index.html all_posts posts_list readings.html

CONTENTS =  head_contents.html \
			navbar.html


index.html: renders/index_render.html $(CONTENTS)
	$(shell python render_index.py renders/index_render.html index.html)

readings.html: renders/readings_render.html $(CONTENTS)
	$(shell python render_index.py renders/readings_render.html readings.html)

posts_list: posts_list_template.html $(CONTENTS)
	$(shell python create_posts.py)


renders/readings_render.html: readings.md
	pandoc readings.md -o renders/readings_render.html

renders/index_render.html: index.md
	pandoc index.md -o renders/index_render.html

all_posts:
	./render_posts.sh

clean:
	rm -f renders/*.html
	rm -f renders/posts/*.html
	rm -f index.html
	rm -f posts/*.html
