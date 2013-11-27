from django.utils.safestring import mark_safe
from django import forms

class BonsaiDateWidget(forms.DateTimeInput):
	def render(self, name, value, attrs=None):
		attrs['readonly'] = 'true'
		output = super(BonsaiDateWidget, self).render(name, value, attrs) 
		return mark_safe(u''' 
				<input type="text" name="id_%s" id="id_%s"  	
					dojoType="dijit.form.DateTextBox"/>
				<input type="text" name="id_%s_time" id="id_%s_time"  	
					dojoType="dijit.form.TimeTextBox"/>

			''' % (name, name))

class BonsaiDateTimeWidget(forms.DateTimeInput):
	def render(self, name, value, attrs=None):
		attrs['readonly'] = 'true'
		output = super(BonsaiDateTimeWidget, self).render(name, value, attrs)
		return mark_safe(u'''
                <label for="id_%s_0">Date:</label>
                <input type="text" id="id_%s_0" name="%s_0"/>
                <br />
                <label for="id_%s_1">Time:</label>
                <input type="text" id="id_%s_1" name="%s_1"/>
				<script type="text/javascript">
					$("#id_%s_0").datepicker({ altFormat: 'dd-mm-yyyy', buttonImage: '/site_media/images/calendar-select.png' });
					$('#id_%s_1').timepickr({trigger: '#trigger-test'});
				</script>
			''' % (name, name, name, name, name, name, name, name))
	
