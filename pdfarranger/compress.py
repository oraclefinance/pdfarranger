import gettext

from gi.repository import Gtk

from pdfarranger.croputils import  _RadioStackSwitcher

_ = gettext.gettext


class RadioOption(Gtk.HBox):
    def __init__(self, label):
        super().__init__()
        self.add(Gtk.Label(label="Selected: {}".format(label)))
        # self.add(Gtk.Label(label=_("mm")))
        # # A PDF unit is 1/72 inch
        # self.entry.set_value(default * 25.4 / 72)

    def get_value(self):
        return self.entry.get_value() / 25.4 * 72


class Dialog(Gtk.Dialog):
    """ A dialog box to define margins for page cropping and page size or scale factor """

    def __init__(self, model, window):
        super().__init__(
            title=_("Compression"),
            parent=window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
            ),
        )
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_resizable(False)
        small_widget = RadioOption((_("Small")))
        smaller_widget = RadioOption((_("Smaller")))

        self.scale_stack = _RadioStackSwitcher()
        self.scale_stack.add_named(small_widget, "Small", _("Small"))
        self.scale_stack.add_named(smaller_widget, "Smaller", _("Smaller"))
        frame = Gtk.Frame(label=_("Intensity"))
        frame.props.margin = 8
        frame.props.margin_bottom = 0
        frame.add(self.scale_stack)

        label = Gtk.Label()
        label.set_text(
            "If the Smaller option is toggled then the outcome will use a \ndifferent method that usually results in smaller file sizes.")
        self.vbox.pack_start(label, True, True, 0)
        self.vbox.pack_start(frame, True, True, 0)

        self.show_all()

    def run_get(self):
        """ Open the dialog and return the crop value """
        result = self.run()
        ok = None
        compress_type = None
        if result == Gtk.ResponseType.OK:
            ok = True
            compress_type = self.scale_stack.selected_name
        self.destroy()
        return ok, compress_type
