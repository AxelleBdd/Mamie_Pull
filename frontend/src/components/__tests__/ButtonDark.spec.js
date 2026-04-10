import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ButtonDark from '../ButtonDark.vue'

describe('ButtonDark', () => {
  it('renders default button text from props', () => {
    const wrapper = mount(ButtonDark, {
      props: {
        buttonText: 'Test button',
        buttonType: 'submit',
      },
    })

    expect(wrapper.text()).toBe('Test button')
    expect(wrapper.attributes('type')).toBe('submit')
  })

  it('emits click event when the button is clicked', async () => {
    const wrapper = mount(ButtonDark, {
      slots: {
        default: 'Click me',
      },
    })

    await wrapper.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('click')
    expect(wrapper.emitted('click')[0]).toHaveLength(1)
  })
})