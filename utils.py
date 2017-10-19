from discord import Embed


def makeEmbed(**kwargs):

    """
    Creates an embed messasge with specified inputs.
    Parameters
    ----------
        author
        author_url
        author_icon
        user
        colour
        fields
        inline
        thumbnail
        image
        footer
        footer_icon
    """

    # Get the attributes from the user
    Empty = Embed.Empty
    if True:
        # Get the author/title information
        author = kwargs.get('author', Empty)
        author_url = kwargs.get('author_url', Empty)
        author_icon = kwargs.get('author_icon', Empty)
        user = kwargs.get('user', None)

        # Get the colour
        colour = kwargs.get('colour', 0)

        # Get the values
        fields = kwargs.get('fields', {})
        inline = kwargs.get('inline', True)
        description = kwargs.get('description', Empty)

        # Footer
        footer = kwargs.get('footer', Empty)
        footer_icon = kwargs.get('footer_icon', Empty)

    # Filter the colour into a usable form
    if type(colour).__name__ == 'Message':
        colour = colour.author.colour.value
    elif type(colour).__name__ == 'Server':
        colour = colour.me.colour.value
    elif type(colour).__name__ == 'Member':
        colour = colour.colour.value

    # Create an embed object with the specified colour
    embedObj = Embed(colour=colour)

    # Set the normal attributes
    if author != Empty:
        embedObj.set_author(name=author, url=author_url, icon_url=author_icon)
    embedObj.set_footer(text=footer, icon_url=footer_icon)
    embedObj.description = description

    # Set the fields
    for i, o in fields.items():
        p = inline
        if type(o) in [tuple, list]:
            p = o[1]
            o = o[0]
        embedObj.add_field(name=i, value=o, inline=p)

    # Return to user
    return embedObj
