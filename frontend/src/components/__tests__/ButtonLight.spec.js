import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ButtonLight from '../ButtonLight.vue'

describe('ButtonLight', () => {
  it('renders default button text from props', () => {
    const wrapper = mount(ButtonLight, {
      props: {
        buttonText: 'Test button',
        buttonType: 'submit',
      },
    })

    expect(wrapper.text()).toBe('Test button')
    expect(wrapper.attributes('type')).toBe('submit')
  })

  it('emits click event when the button is clicked', async () => {
    const wrapper = mount(ButtonLight, {
      slots: {
        default: 'Click me',
      },
    })

    await wrapper.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('click')
    expect(wrapper.emitted('click')[0]).toHaveLength(1)
  })
})