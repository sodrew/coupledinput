"""Add the ability to show two responses for a prompt."""
import pkg_resources
from webob import Response
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, String, Scope
from django.template import Context, Template
import unicodecsv
from io import BytesIO as StringIO


class CoupledInputXBlock(XBlock):
    """Displays names, and two boxes for each response."""

    # Scope.content
    # (for all users, one block, all runs)
    display_name = String(
        display_name="Coupled Input",
        default="Coupled Input",
        scope=Scope.settings,
        help='The title Studio uses for the component.',
    )

    prompt = String(
        display_name="Prompt",
        default="",
        scope=Scope.settings,
        help="Prompt for users",
    )

    show_names = Boolean(
        display_name="Show Names",
        default=False,
        scope=Scope.settings,
        help="Whether to show the input fields for user names",
    )

    hide_one = Boolean(
        display_name="Hide User Response One",
        default=False,
        scope=Scope.settings,
        help="Whether to hide the input fields for response one",
    )

    hide_two = Boolean(
        display_name="Hide User Response Two",
        default=False,
        scope=Scope.settings,
        help="Whether to hide the input fields for response two",
    )

    show_reversed = Boolean(
        display_name="Reverse Order",
        default=False,
        scope=Scope.settings,
        help="Whether to show the input fields user two first",
    )

    show_abbrev = Boolean(
        display_name="Abbreviated Inputs",
        default=False,
        scope=Scope.settings,
        help="Whether to show smaller side by side inputs",
    )

    # Scope.settings
    # (for all users, one block, one run)

    # Scope.preferences
    # (for one user, all blocks, all runs)
    username_one = String(
        display_name="User Name One",
        default="User One",
        scope=Scope.preferences,
        help="User One entry",
    )

    username_two = String(
        display_name="User Name Two",
        default="User Two",
        scope=Scope.preferences,
        help="User Two entry",
    )

    # Scope.user_state
    # (for one user, one block, one run)
    response_one = String(
        display_name="Response One",
        default="",
        scope=Scope.user_state,
        help="User One entry",
    )

    response_two = String(
        display_name="Response Two",
        default="",
        scope=Scope.user_state,
        help="User Two entry",
    )

    # ensure author_view gets called in studio
    has_author_view = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(self, template_path, context={}):
        """Enable django template tags."""
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

    def load_studio_html(self):
        """Load studio html helper function."""
        return self.render_template(
            "static/html/coupledinput_studio.html",
            {'show_names_is_checked':
             'checked' if self.show_names else '',
             'hide_one_is_checked':
             'checked' if self.hide_one else '',
             'hide_two_is_checked':
             'checked' if self.hide_two else '',
             'show_reversed_is_checked':
             'checked' if self.show_reversed else '',
             'show_abbrev_is_checked':
             'checked' if self.show_abbrev else '',
             })

    def student_view(self, context=None):
        """View for the student."""
        if self.show_names:
            html = self.resource_string("static/html/coupledinput_user.html")
        else:
            html = self.render_template("static/html/coupledinput.html",
                                        {'hide_one': self.hide_one,
                                         'hide_two': self.hide_two,
                                         'show_reversed': self.show_reversed,
                                         'show_abbrev': self.show_abbrev,
                                         })

        # adding code to make it easier to test
        if (context and 'activate_block_id' in context and
           context['activate_block_id'] is None):
            test_html = self.load_studio_html()
            html += '<hr><br>' + test_html
        # else:
        #     print('context-------', context)
        #     self.get_blocks_of_type(str(self.course_id), self.category)

        frag = Fragment(html.format(self=self))

        if context and 'coupledinput' in context:
            frag.add_css(self.resource_string(
                "static/css/coupledinput_studio.css"))
        else:
            frag.add_css(self.resource_string(
                "static/css/coupledinput.css"))
        frag.add_javascript(self.resource_string(
            "static/js/src/coupledinput.js"))
        frag.initialize_js('CoupledInputXBlock')
        return frag

    def author_view(self, context={}):
        """Preview of student_view for the instructor."""
        context['coupledinput'] = 'author'

        return self.student_view(context)

    def studio_view(self, context=None):
        """View for the instructor."""
        html = self.load_studio_html()
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/coupledinput.css"))
        frag.add_javascript(self.resource_string(
            "static/js/src/coupledinput.js"))
        frag.initialize_js('CoupledInputXBlock')
        return frag

    def send_json_save_status(self, changed):
        """Return a response to the UI."""
        if changed:
            return {'message': 'Saved!',
                    'color': 'green',
                    'changed': True}
        else:
            return {'message': 'No changes to save.',
                    'color': 'black',
                    'changed': False}

    @XBlock.json_handler
    def save_studio(self, data, suffix=''):
        """Save the prompt by the instructor."""
        prompt = data.get('prompt', '')
        s_names = data.get('show_names', False)
        h_one = data.get('hide_one', False)
        h_two = data.get('hide_two', False)
        s_reversed = data.get('show_reversed', False)
        s_abbrev = data.get('show_abbrev', False)

        changed = False

        if prompt != self.prompt:
            self.prompt = prompt
            changed = True
        if s_names != self.show_names:
            self.show_names = s_names
            changed = True
        if h_one != self.hide_one:
            self.hide_one = h_one
            changed = True
        if h_two != self.hide_two:
            self.hide_two = h_two
            changed = True
        if s_reversed != self.show_reversed:
            self.show_reversed = s_reversed
            changed = True
        if s_abbrev != self.show_abbrev:
            self.show_abbrev = s_abbrev
            changed = True
        return self.send_json_save_status(changed)

    @XBlock.json_handler
    def save_response(self, data, suffix=''):
        """Save the response by the user."""
        r_one = data.get('response_one', '')
        r_two = data.get('response_two', '')
        changed = False

        if r_one != self.response_one:
            self.response_one = r_one
            changed = True
        if r_two != self.response_two:
            self.response_two = r_two
            changed = True

        from .models import CoupledInputResponse
        if changed:
            try:
                user_id = self.runtime.user_id
                print('0----------------------------')
                print('course: ', len(str(self.course_id)),
                      str(self.course_id))
                print('user: ', len(str(user_id)), str(user_id))
                print('block: ', len(str(self.location.block_id)),
                      str(self.location.block_id))
                data, _ = CoupledInputResponse.objects.get_or_create(
                    course_id=str(self.course_id),
                    student_id=user_id,
                    block_id=self.location.block_id,
                )
                data.prompt = self.prompt
                data.response_one = r_one
                data.response_two = r_two
                data.save()
            except Exception as e:
                # Handle any other unexpected exceptions
                print("Error while saving to DB:", e)

        return self.send_json_save_status(changed)

    @XBlock.json_handler
    def save_names(self, data, suffix=''):
        """Save the names by the user."""
        r_one = data.get('response_one', '')
        r_two = data.get('response_two', '')
        changed = False

        if r_one != self.username_one:
            self.username_one = r_one
            changed = True
        if r_two != self.username_two:
            self.username_two = r_two
            changed = True

        from .models import CoupledInputUser
        if changed:

            user_id = self.runtime.user_id
            user_name = self.get_user_name(user_id)
            data, _ = CoupledInputUser.objects.get_or_create(
                course_id=str(self.course_id),
                student_id=user_id,
            )
            data.student_name = user_name
            data.name_one = r_one
            data.name_two = r_two
            data.save()

        return self.send_json_save_status(changed)

    @XBlock.handler
    def export_csv(self, request, suffix=''):
        """Handle the export click."""
        response = Response(content_type='text/csv')
        response.app_iter = self.get_csv()
        response.content_disposition = 'attachment; filename=course_data.csv'
        return response

    def get_csv(self):
        """Provide the CSV data."""
        from .models import CoupledInputResponse, CoupledInputUser

        course_id = str(self.course_id)
        print('course_id', course_id)
        # retrieve all of the users names for the course
        users = CoupledInputUser.objects.filter(
            course_id=course_id,
        ).order_by('student_id')

        # create a username lookup dict
        users_lookup = {user.student_id: user.to_val_list() for user in users}

        # retrieve all of the responses for the course
        responses = CoupledInputResponse.objects.filter(
            course_id=course_id,
        ).order_by('student_id')

        buf = StringIO()
        writer = unicodecsv.writer(buf, encoding='utf-8')
        writer.writerow([
            'course_id',
            'student_id',
            'student_name',
            'user_one',
            'user_two',
            'block_id',
            'prompt',
            'response_one',
            'response_two',
        ])

        print("yo")

        for response in responses:
            if response.student_id in users_lookup:
                user = users_lookup[response.student_id]
            else:
                user = [
                        'unknown student',
                        'unknown 1',
                        'unknown 2',
                        ]
            print(user)

            row = [course_id, response.student_id]
            row += user
            row += response.to_val_list()
            print(row)
            writer.writerow([
                'course_id',
                'student_id',
                'student_name',
                'user_one',
                'user_two',
                'block_id',
                'prompt',
                'response_one',
                'response_two',
            ])
        buf.seek(0)
        return buf.read()


    # def get_blocks_of_type(self, course_id, block_type):
    #     from opaque_keys.edx.keys import CourseKey
    #     from xmodule.modulestore.django import modulestore
    #     from xmodule.modulestore.exceptions import ItemNotFoundError
    #     course_key = CourseKey.from_string(course_id)
    #     block_list = []

    #     try:
    #         # course = modulestore().get_course(course_key)
    #         # print(f"got course: {course}")
    #         for item in modulestore().get_items(course_key,
    #                                             block_type_id=block_type):
    #             # print(f"got item: {item}")
    #             try:
    #                 block = modulestore().get_item(item.location, depth=0)
    #                 if isinstance(block, CoupledInputXBlock):
    #                     print(f"Block ID: {block.location.block_id}")
    #                     print("Block prompt: ", block.get_all_user_responses())
    #                     print("\n")
    #                     block_list.append(block)
    #             except ItemNotFoundError:
    #                 pass
    #     except Exception as e:
    #         # Handle exceptions as needed
    #         print(f"Error: {e}")

    #     return block_list

    # TO-DO:change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """Display different scenarios in the workbench."""
        return [
            ("CoupledInputXBlock",
             """<coupledinput/>
             """),
            ("Multiple CoupledInputXBlock",
             """<vertical_demo>
                <coupledinput/>
                <coupledinput/>
                <coupledinput/>
                </vertical_demo>
             """),
        ]
