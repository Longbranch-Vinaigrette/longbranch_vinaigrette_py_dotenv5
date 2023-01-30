from .DotEnvLine import DotEnvLine


class DotEnvLines:
    comments_keyword = "_dot_env_parser_comments"

    def __init__(self,
                 lines: list,
                 with_comments: bool = False,
                 debug: bool = False):
        self.lines = lines
        self.with_comments = with_comments
        self.debug = debug

    def parse_lines(self) -> dict:
        """Lines parser"""
        env_vars: dict = {}
        last_line_var_name = ""

        for index, line in enumerate(self.lines):
            line: str = line
            dot_env_line = DotEnvLine(line)

            if self.debug:
                print(line)

            # Check if it's empty
            if dot_env_line.is_line_empty():
                # Next
                continue

            # A line may end with a '\', indicating that it continues
            if dot_env_line.does_line_continues():
                if self.debug:
                    print("Is a continuing line.")

                if not last_line_var_name:
                    if self.debug:
                        print("This is the first line.")
                    # This is the first line
                    env_var = DotEnvLine(line)
                    env_vars[env_var.get_var_name()] = env_var.get_value()
                    last_line_var_name = env_var.get_var_name()

                # The whole line should be added
                env_vars[last_line_var_name] += line
            else:
                try:
                    # Comments
                    if dot_env_line.is_line_a_comment():
                        if self.with_comments:
                            env_vars[self.comments_keyword + str(index)] = line
                            # It should end here
                            continue
                        else:
                            continue

                    # If this is a normal line it won't throw an error
                    env_var = DotEnvLine(line)
                    env_vars[env_var.get_var_name()] = env_var.get_value()

                    # Normal line
                    if self.debug:
                        print("Is a normal line.")

                    last_line_var_name = ""
                except:
                    if self.debug:
                        print("Is a continuing line.")

                    # If this throws an exception, it means that the previous lines may have
                    # been like this:
                    # [Some text] \
                    #    Final text             <- We are in this line
                    # NEXT_ENV_VAR=[something]
                    # Now we still have 'last_line_var_name'
                    # so we can just add the whole line and that's it.
                    env_vars[last_line_var_name] += line

                    # Reset it
                    last_line_var_name = ""
        return env_vars
